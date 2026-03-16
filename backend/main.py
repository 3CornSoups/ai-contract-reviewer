"""
=============================================================================
文件作用：FastAPI应用主入口文件，包含路由注册与应用初始化逻辑
创建时间：2026-03-15
依赖项：fastapi, uvicorn
修改日志：
  2026-03-15: 初始创建，注册API路由
=============================================================================
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import endpoints

def create_app() -> FastAPI:
    """
    创建并配置FastAPI应用实例
    
    参数:
        无
        
    返回:
        FastAPI: 配置好的应用实例
        
    异常:
        无
    """
    app = FastAPI(
        title="AI合同智能审核系统 API",
        description="基于 LLM 和 RAG 的合同审核及法律知识库管理系统",
        version="1.0.0"
    )
    
    # 配置CORS (实际生产中交由Nginx处理，此处为开发联调备用)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 注册路由
    app.include_router(endpoints.router, prefix="/api")
    
    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
