-- =========================================================================
-- 文件作用：初始化PostgreSQL数据库，创建业务表及开启向量扩展
-- 创建时间：2026-03-15
-- 依赖项：需要PostgreSQL安装了 pgvector 插件
-- 修改日志：
--   2026-03-15: 初始创建
-- =========================================================================

-- 1. 开启 pgvector 扩展 (关键配置，用于支持向量存储和检索)
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. 创建用户表
-- 目的: 存储系统操作用户，用于简单鉴权
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL, -- 用户名
    password_hash VARCHAR(255) NOT NULL,  -- 密码哈希值
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 初始化一个默认管理员账户 (密码为 admin123 的简单哈希示例，实际中应由后端 bcrypt 生成)
-- 仅供测试使用
INSERT INTO users (username, password_hash) VALUES ('admin', 'fake_hash_for_admin') ON CONFLICT DO NOTHING;

-- 3. 创建知识库文档表
-- 目的: 记录上传的法律法规文档元数据
CREATE TABLE IF NOT EXISTS knowledge_docs (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,        -- 文件名
    file_path TEXT NOT NULL,               -- 存储路径
    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. 创建法条向量分块表
-- 目的: 存储法律文档的具体文本分块及其对应的向量，用于RAG相似度检索
CREATE TABLE IF NOT EXISTS knowledge_chunks (
    id SERIAL PRIMARY KEY,
    doc_id INTEGER REFERENCES knowledge_docs(id) ON DELETE CASCADE, -- 关联文档
    content TEXT NOT NULL,                 -- 文本分块内容
    embedding vector(1536)                 -- 向量字段 (OpenAI text-embedding-ada-002 通常为 1536 维)
);

-- 为向量字段创建索引 (使用 HNSW 索引以加速相似度检索)
-- 修改注意事项: lists的参数应根据数据量调整，数据量较小可不建索引，此处提供标准化建立方式
CREATE INDEX ON knowledge_chunks USING hnsw (embedding vector_cosine_ops);

-- 5. 创建审核记录表
-- 目的: 保存合同审核的历史结果
CREATE TABLE IF NOT EXISTS audit_records (
    id SERIAL PRIMARY KEY,
    contract_filename VARCHAR(255) NOT NULL, -- 审核的合同名称
    audit_result JSONB NOT NULL,             -- 结构化的审核结果 (包含违规点、建议等)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. 操作日志表 (用于审计与问题排查)
-- 目的: 记录关键操作（上传知识库、合同审核等）的时间、类型、关联文件名等
CREATE TABLE IF NOT EXISTS operation_logs (
    id SERIAL PRIMARY KEY,
    operation_type VARCHAR(50) NOT NULL,     -- 如: knowledge_upload, contract_audit
    detail TEXT,                             -- 简要说明，如文件名、doc_id
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
