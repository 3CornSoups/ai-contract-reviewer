"""
=============================================================================
文件作用：定义系统的核心 API 接口路由（上传、检索、审核）
创建时间：2026-03-15
依赖项：fastapi, sqlalchemy
修改日志：
  2026-03-15: 初始创建，实现知识库上传与合同审核API
=============================================================================
"""

import os
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from core.database import get_db
from models.schemas import User
from utils.pdf_parser import PDFParser
from utils.llm_client import LLMClient
from utils.vector_store import VectorStore

router = APIRouter()


class LoginRequest(BaseModel):
    """登录请求体"""
    username: str
    password: str


@router.post("/login", summary="用户登录")
async def login(body: LoginRequest, db: Session = Depends(get_db)):
    """
    简单登录校验：校验用户名与密码后返回占位 token。
    生产环境建议使用 bcrypt 校验 password_hash 并签发 JWT。
    """
    user = db.query(User).filter(User.username == body.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    # 演示环境：与 init.sql 中占位一致时通过（生产应使用 bcrypt.verify）
    if body.password != "admin123" or user.password_hash != "fake_hash_for_admin":
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    return {"token": "demo_token", "username": body.username}

# 确保存储目录存在
UPLOAD_DIR = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/knowledge/upload", summary="上传法律文档至知识库")
async def upload_knowledge_doc(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    接口功能：接收PDF格式的法律法规文档，解析文本，切块，向量化后存入 pgvector
    
    请求参数:
        - file (UploadFile, 必填): 待上传的PDF文件
        
    响应:
        - doc_id (int): 入库成功后的文档主键
        - message (str): 状态提示
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="仅支持 PDF 格式文件")
        
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    # 1. 保存文件到本地临时目录
    with open(file_path, "wb") as f:
        f.write(await file.read())
        
    try:
        # 2. 解析PDF提取纯文本
        text = PDFParser.extract_text(file_path)
        
        # 3. 文本分块 (Chunking)
        chunks = PDFParser.chunk_text(text, chunk_size=500, chunk_overlap=50)
        
        # 4. 批量调用Embedding模型获取向量
        embeddings = [LLMClient.get_embedding(chunk) for chunk in chunks]
        
        # 5. 存入PostgreSQL(pgvector)
        doc_id = VectorStore.save_knowledge_doc(db, file.filename, file_path, chunks, embeddings)
        VectorStore.log_operation(db, "knowledge_upload", f"filename={file.filename}, doc_id={doc_id}, chunks={len(chunks)}")
        
        return {"status": "success", "doc_id": doc_id, "message": f"成功入库 {len(chunks)} 个知识块"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件处理失败: {str(e)}")

@router.post("/contract/audit", summary="智能审核合同文件")
async def audit_contract(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    接口功能：上传待审核合同PDF，触发RAG检索（找出相关法条），并交由LLM进行比对审核
    
    请求参数:
        - file (UploadFile, 必填): 待审核的合同PDF文件
        
    响应:
        - status (str): "PASS" 或 "FAIL"
        - risk_level (str): 风险等级
        - violations (List): 具体的违规项、依据及建议
        - summary (str): 总体概述
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="仅支持 PDF 格式文件")
        
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
        
    try:
        # 1. 解析合同文本
        contract_text = PDFParser.extract_text(file_path)
        
        # 为了避免超大合同超出模型上下文限制，先取整篇合同的概要或核心前 N 字符做 embedding 检索，
        # 生产环境中应对合同也进行 chunking 遍历检索。此处简化逻辑，直接对合同整体/部分做检索。
        truncated_contract = contract_text[:1500] if len(contract_text) > 1500 else contract_text
        
        # 2. 生成合同文本的特征向量
        contract_embedding = LLMClient.get_embedding(truncated_contract)
        
        # 3. RAG 召回：检索知识库中最相关的法条片段 (Top 3)
        relevant_docs = VectorStore.search_similar_chunks(db, contract_embedding, top_k=3)
        reference_text = "\n\n---\n\n".join(relevant_docs)
        
        # 4. 将合同内容及参考法条组装为 Prompt，调用 LLM 审核
        audit_result = LLMClient.audit_contract(truncated_contract, reference_text)
        
        # 5. 存储审核记录并写操作日志
        VectorStore.save_audit_record(db, file.filename, audit_result)
        VectorStore.log_operation(db, "contract_audit", f"filename={file.filename}")
        
        return audit_result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"审核失败: {str(e)}")
