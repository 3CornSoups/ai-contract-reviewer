# api 模块

本目录存放 FastAPI 的路由与接口定义。

- **endpoints.py**：核心 API 实现，包括 `/knowledge/upload`（知识库上传）、`/contract/audit`（合同审核）。所有接口均以 `/api` 为前缀在 `main.py` 中挂载。
