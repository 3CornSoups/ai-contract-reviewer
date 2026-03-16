"""
=============================================================================
文件作用：读取和管理系统环境变量配置
创建时间：2026-03-15
依赖项：pydantic_settings
修改日志：
  2026-03-15: 初始创建
=============================================================================
"""

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    系统配置管理类，自动从环境变量或 .env 文件加载参数
    """
    PROJECT_NAME: str = "AI Contract Reviewer"
    
    # 数据库连接配置 (默认指向docker-compose的postgres服务)
    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/contract_db"
    
    # LLM/OpenAI 兼容配置
    OPENAI_API_KEY: str = "your_api_key_here"
    OPENAI_API_BASE: str = "https://api.openai.com/v1"
    EMBEDDING_MODEL: str = "text-embedding-ada-002"
    CHAT_MODEL: str = "gpt-4"
    
    # JWT 秘钥（仅占位，系统当前采用简单鉴权或依赖网关）
    SECRET_KEY: str = "your-secret-key"
    
    class Config:
        env_file = ".env"

settings = Settings()
