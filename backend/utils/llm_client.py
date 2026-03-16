"""
=============================================================================
文件作用：封装与大模型（OpenAI API格式）交互的客户端接口
创建时间：2026-03-15
依赖项：openai (v0.28.1)，兼容多种本地及三方模型
修改日志：
  2026-03-15: 初始创建
=============================================================================
"""

import openai
import json
from typing import List, Dict, Any
from core.config import settings

# 初始化全局API配置
openai.api_key = settings.OPENAI_API_KEY
openai.api_base = settings.OPENAI_API_BASE

class LLMClient:
    """
    大模型及Embedding模型的封装客户端
    """
    
    @staticmethod
    def get_embedding(text: str) -> List[float]:
        """
        调用 Embedding API 获取文本的高维向量表示
        
        参数:
            text (str): 待向量化的纯文本
            
        返回:
            List[float]: 浮点数向量数组，用于 pgvector 存储与检索
            
        异常:
            抛出 openai.error.OpenAIError 若请求失败
        """
        response = openai.Embedding.create(
            input=text,
            model=settings.EMBEDDING_MODEL
        )
        return response['data'][0]['embedding']
        
    @staticmethod
    def audit_contract(contract_text: str, reference_docs: str) -> Dict[str, Any]:
        """
        调用 LLM 审核合同文本（结合RAG检索到的相关法条参考）
        
        参数:
            contract_text (str): 待审核的合同正文
            reference_docs (str): RAG召回的相关法律条款文本，用于作为 Prompt 依据
            
        返回:
            Dict: 包含审核结果（违规点、风险等级、建议）的结构化 JSON 字典
        """
        prompt = f"""
        你是一个资深的法务合同审核专家。
        请仔细阅读以下【待审合同内容】，并严格按照提供的【参考法律条款】进行合规审查。
        如果发现合同条款与参考法律条款存在冲突或遗漏，请指出违规点。
        如果没有冲突，请说明“未发现明显违规”。

        【参考法律条款】:
        {reference_docs}

        【待审合同内容】:
        {contract_text}

        请以严格的 JSON 格式返回审核结果，不包含任何外部说明，JSON 结构如下:
        {{
            "status": "PASS" | "FAIL",
            "risk_level": "None" | "Low" | "Medium" | "High",
            "violations": [
                {{
                    "issue": "违规或遗漏点描述",
                    "basis": "对应的参考法律条款依据",
                    "suggestion": "修改建议"
                }}
            ],
            "summary": "整体审核结论概述"
        }}
        """
        
        response = openai.ChatCompletion.create(
            model=settings.CHAT_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that strictly outputs JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1 # 使用低 temperature 保证输出的稳定性和客观性
        )
        
        result_text = response['choices'][0]['message']['content']
        # 尝试剥离 Markdown 的 JSON 代码块，确保返回可解析的字典
        try:
            if result_text.startswith("```json"):
                result_text = result_text.replace("```json", "").replace("```", "").strip()
            return json.loads(result_text)
        except json.JSONDecodeError as e:
            return {"error": "LLM返回了非标准的JSON格式", "raw_output": result_text}
