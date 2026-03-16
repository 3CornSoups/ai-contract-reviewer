# utils 模块

本目录存放与业务无关的工具类。

- **pdf_parser.py**：PDF 文本提取（pdfplumber）与按字符数分块（含重叠）。
- **llm_client.py**：调用 OpenAI 兼容接口获取 Embedding 与合同审核结果（封装 Prompt 与 JSON 解析）。
- **vector_store.py**：对 pgvector 的封装，包括知识库文档/分块写入与基于余弦相似度的检索。
