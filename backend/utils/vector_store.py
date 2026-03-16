"""
=============================================================================
文件作用：封装 pgvector 数据库的常用向量操作，包含插入、相似度检索
创建时间：2026-03-15
依赖项：sqlalchemy, pgvector, models.schemas
修改日志：
  2026-03-15: 初始创建
=============================================================================
"""

from sqlalchemy.orm import Session
from models.schemas import KnowledgeDoc, KnowledgeChunk, AuditRecord, OperationLog
from typing import List, Tuple

class VectorStore:
    """
    知识库文档管理与向量检索操作类
    """
    
    @staticmethod
    def save_knowledge_doc(db: Session, filename: str, file_path: str, chunks: List[str], embeddings: List[List[float]]) -> int:
        """
        保存法律法规文档及其切分后的向量分块
        
        参数:
            db (Session): 数据库会话
            filename (str): 文件名称
            file_path (str): 存储路径
            chunks (List[str]): 文本块数组
            embeddings (List[List[float]]): 对应的向量数组
            
        返回:
            int: 插入的文档记录的主键ID
        """
        # 保存主文档
        doc = KnowledgeDoc(filename=filename, file_path=file_path)
        db.add(doc)
        db.commit()
        db.refresh(doc)
        
        # 批量保存文本块及向量
        db_chunks = []
        for text, vector in zip(chunks, embeddings):
            chunk_record = KnowledgeChunk(
                doc_id=doc.id,
                content=text,
                embedding=vector
            )
            db_chunks.append(chunk_record)
            
        db.add_all(db_chunks)
        db.commit()
        return doc.id

    @staticmethod
    def search_similar_chunks(db: Session, query_embedding: List[float], top_k: int = 3) -> List[str]:
        """
        利用 pgvector 进行向量相似度检索 (RAG核心逻辑)
        
        参数:
            db (Session): 数据库会话
            query_embedding (List[float]): 待检索文本的向量
            top_k (int): 返回最相似的记录数
            
        返回:
            List[str]: 最匹配的知识库文本片段列表
        """
        # 核心 SQL 构建：使用 pgvector 的 `<=>` 运算符计算余弦相似度并排序
        # SQLAlchemy ORM 提供了 `.cosine_distance()` 方法或 `embedding.l2_distance()`
        # 这里使用 HNSW 建立的 Cosine (余弦) 距离查询
        results = db.query(KnowledgeChunk).order_by(
            KnowledgeChunk.embedding.cosine_distance(query_embedding)
        ).limit(top_k).all()
        
        return [record.content for record in results]

    @staticmethod
    def save_audit_record(db: Session, filename: str, result: dict) -> int:
        """
        保存合同审核结果记录
        """
        record = AuditRecord(
            contract_filename=filename,
            audit_result=result
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record.id

    @staticmethod
    def log_operation(db: Session, operation_type: str, detail: str = None) -> None:
        """
        写入操作日志，便于审计与问题排查。
        参数: db 数据库会话; operation_type 操作类型(如 knowledge_upload, contract_audit); detail 可选说明。
        """
        log = OperationLog(operation_type=operation_type, detail=detail)
        db.add(log)
        db.commit()
