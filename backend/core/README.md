# core 模块

本目录存放应用的核心配置与基础设施代码。

- **config.py**：基于 pydantic-settings 的环境变量配置（数据库连接、OpenAI API、密钥等）。
- **database.py**：SQLAlchemy 引擎与 Session 的创建，以及依赖注入用的 `get_db()`。
