# API 接口文档

## 1. 概述
本文档描述 AI合同智能审核系统 后端的所有 RESTful API 接口。所有请求及响应的数据格式均为 JSON，除文件上传采用 `multipart/form-data` 格式外。接口统一由网关转发，访问前缀为 `/api/`。

## 2. 接口列表

### 2.1 用户登录
- **路径**: `/api/login`
- **请求方法**: `POST`
- **请求格式**: `application/json`
- **请求参数**: Body JSON `{"username": "admin", "password": "admin123"}`
- **响应 200**: `{"token": "demo_token", "username": "admin"}`
- **响应 401**: `{"detail": "用户名或密码错误"}`

### 2.2 上传法律文档至知识库
接收包含法律法规文本的 PDF 文件，将其切分并存入向量数据库中。

- **路径**: `/api/knowledge/upload`
- **请求方法**: `POST`
- **请求格式**: `multipart/form-data`
- **请求参数**:
  - `file` (文件类型, 必填): 待上传的 PDF 文件。例如 `contract_law_2021.pdf`。
- **响应格式**: JSON
- **状态码 200 成功响应示例**:
```json
{
  "status": "success",
  "doc_id": 1,
  "message": "成功入库 12 个知识块"
}
```
- **状态码 400/500 失败响应示例**:
```json
{
  "detail": "仅支持 PDF 格式文件"
}
```

### 2.3 智能审核合同文件
上传一份待审核合同文档，触发 RAG（基于法条增强生成）大模型审核流程。

- **路径**: `/api/contract/audit`
- **请求方法**: `POST`
- **请求格式**: `multipart/form-data`
- **请求参数**:
  - `file` (文件类型, 必填): 待审核的合同 PDF 文件。
- **响应格式**: JSON
- **状态码 200 成功响应示例**:
```json
{
  "status": "FAIL",
  "risk_level": "High",
  "violations": [
    {
      "issue": "违约金比例超过法定上限",
      "basis": "根据《民法典》第五百八十五条规定，约定的违约金过分高于造成的损失的，人民法院或者仲裁机构可以根据当事人的请求予以适当减少。",
      "suggestion": "建议将违约金比例从每日 0.5% 调整为每日 0.05%。"
    }
  ],
  "summary": "合同存在较高的合规风险，主要集中在违约金及保密期限条款，建议法务二次人工复核。"
}
```
- **调用示例 (cURL)**:
```bash
curl -X POST "http://localhost:8000/api/contract/audit" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@/path/to/test_contract.pdf"
```