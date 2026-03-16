"""
=============================================================================
文件作用：定义SQLAlchemy实体模型，包括向量表的映射
创建时间：2026-03-15
依赖项：sqlalchemy, pgvector
修改日志：
  2026-03-15: 初始创建
=============================================================================
"""

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from core.database import Base
import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class KnowledgeDoc(Base):
    __tablename__ = "knowledge_docs"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(Text, nullable=False)
    upload_time = Column(DateTime, default=datetime.datetime.utcnow)
    
    chunks = relationship("KnowledgeChunk", back_populates="document", cascade="all, delete-orphan")

class KnowledgeChunk(Base):
    __tablename__ = "knowledge_chunks"
    
    id = Column(Integer, primary_key=True, index=True)
    doc_id = Column(Integer, ForeignKey("knowledge_docs.id", ondelete="CASCADE"))
    content = Column(Text, nullable=False)
    # 假设使用 text-embedding-ada-002, 为 1536 维
    embedding = Column(Vector(1536))
    
    document = relationship("KnowledgeDoc", back_populates="chunks")

class AuditRecord(Base):
    __tablename__ = "audit_records"
    
    id = Column(Integer, primary_key=True, index=True)
    contract_filename = Column(String(255), nullable=False)
    audit_result = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class OperationLog(Base):
    """操作日志表 ORM，对应 database/init.sql 中的 operation_logs 表"""
    __tablename__ = "operation_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    operation_type = Column(String(50), nullable=False)
    detail = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
