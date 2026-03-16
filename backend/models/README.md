# models 模块

本目录存放与数据库表对应的 ORM 模型。

- **schemas.py**：定义 `User`、`KnowledgeDoc`、`KnowledgeChunk`（含 pgvector 的 `Vector(1536)` 字段）、`AuditRecord`。表结构以 `database/init.sql` 为准，本模块仅用于读写映射。
