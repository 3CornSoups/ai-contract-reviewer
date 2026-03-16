"""
=============================================================================
文件作用：PDF文档解析及文本分块工具类
创建时间：2026-03-15
依赖项：pdfplumber (高精度文本提取), tiktoken (分词统计)
修改日志：
  2026-03-15: 初始创建
=============================================================================
"""

import pdfplumber
import tiktoken
from typing import List

class PDFParser:
    """
    处理 PDF 解析和文本清洗/分块的工具类
    """
    
    @staticmethod
    def extract_text(file_path: str) -> str:
        """
        从指定路径的 PDF 提取纯文本
        
        参数:
            file_path (str): PDF 文件的绝对/相对路径
            
        返回:
            str: 提取并简单清洗后的字符串
            
        异常:
            抛出 IOError 若文件读取失败
        """
        text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            raise Exception(f"PDF解析失败: {str(e)}")
            
        # 简单清洗连续换行和空格
        return text.replace("\n\n", "\n").strip()

    @staticmethod
    def chunk_text(text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> List[str]:
        """
        按字符数对长文本进行分块，支持重叠(Overlap)以防止截断语义
        
        参数:
            text (str): 原始长文本
            chunk_size (int): 每个块的最大字符长度
            chunk_overlap (int): 块与块之间的重叠字符数
            
        返回:
            List[str]: 文本块数组
        """
        if not text:
            return []
            
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            
            # 若已经到达末尾，结束循环
            if end >= text_length:
                break
                
            # 步进，考虑重叠部分
            start += (chunk_size - chunk_overlap)
            
        return chunks
