# 测试资源目录

本目录用于存放与《测试说明》配套的测试用文件及脚本。

## 测试用 PDF 文件
请自行准备或放置以下两类 PDF（勿提交涉密或真实合同）：

- **法律文档**：如《民法典》节选、某部门规章全文等，用于「法律知识库管理」上传与向量化。
- **待审合同**：可为一份简易合同（含违约金、保密条款等），用于「合同智能审核」功能验证。

将上述 PDF 放入本目录后，在 cURL 或 Postman 中把路径改为 `@./tests/你的文件名.pdf` 即可。

## 接口测试示例 (Postman)
1. 新建请求，方法为 **POST**，URL 为 `http://localhost/api/knowledge/upload` 或 `http://localhost/api/contract/audit`。
2. 在 **Body** 中选择 **form-data**，添加 key 为 `file`、类型为 **File** 的字段，并选择本地 PDF 文件。
3. 发送请求，根据《API接口文档》与《测试说明》核对状态码与响应 JSON。
