"""
=============================================================================
文件作用：数据库连接池与会话管理，并注册 pgvector 的 SQLAlchemy 类型
创建时间：2026-03-15
依赖项：sqlalchemy, pgvector
修改日志：
  2026-03-15: 初始创建
=============================================================================
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import settings

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    依赖注入：获取数据库会话生成器
    
    参数: 无
    返回: SQLAlchemy Session (Generator)
    异常: 抛出底层数据库连接异常，最终保证会话关闭
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
