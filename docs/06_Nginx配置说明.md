# Nginx 配置说明

## 1. 模块职责
在生产环境中，Nginx 充当整个系统的统一入口网关。其核心职责包括：
- **静态资源托管**：托管 Vue 前端项目构建出来的 `dist` 静态文件。
- **反向代理**：将客户端发往 `/api/` 的请求安全地转发给后端的 FastAPI 服务，解决前后端分离部署的跨域问题。
- **流量控制与安全**：对 API 接口进行访问频率限制，并限制上传文件的大小，防止恶意刷接口和超大文件攻击。

## 2. 核心配置解析

### 2.1 静态资源托管
```nginx
location / {
    root /usr/share/nginx/html;
    index index.html;
    try_files $uri $uri/ /index.html;
}
```
- **配置目的**：前端 Vue 打包后生成 HTML、JS、CSS 文件，Nginx 直接响应这些静态请求，效率极高。`try_files` 配置是为了支持前端单页应用（SPA）的路由模式，当请求的路径在文件系统中找不到时，统一返回 `index.html`，由前端 JS 接管路由渲染。

### 2.2 反向代理与超时设置
```nginx
location /api/ {
    proxy_pass http://backend:8000/api/;
    proxy_read_timeout 300s;
    # ...其他配置...
}
```
- **配置目的**：前端所有的请求只要以 `/api/` 开头，都会被 Nginx 截获并转发给 Docker 内部网络中的 `backend` 容器的 8000 端口。
- **修改注意事项**：因为后端在进行 PDF 解析和调用 LLM 时（特别是长合同）可能需要几十秒到一两分钟，所以这里将 `proxy_read_timeout` 延长到了 `300s`。如果此处未修改，Nginx 会在默认的 60s 后断开连接并向前端返回 `504 Gateway Time-out` 错误。

### 2.3 文件大小限制
```nginx
client_max_body_size 20M;
```
- **配置目的**：Nginx 默认限制上传 body 大小为 1MB。由于我们需要上传 PDF 文件，此处显式放宽到了 20MB。若遇到上传被拒绝且状态码为 `413 Request Entity Too Large`，需检查/修改此项。

### 2.4 API 限流 (Rate Limiting)
```nginx
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=2r/s;
# ...
limit_req zone=api_limit burst=5 nodelay;
```
- **配置目的**：基于客户端的真实 IP 进行限流。配置了每秒最多 2 个请求（`rate=2r/s`），并允许最多 5 个突发请求的排队（`burst=5`）。超过限制的请求将被立即拒绝（`nodelay`）。
- **拦截表现**：被拦截的请求会触发 Nginx 返回 `503 Service Unavailable` 状态码。在 `nginx.conf` 中我们配置了自定义错误页，使其返回 JSON 格式的错误提示：`{"error": "服务访问过于频繁..."}`。

## 3. 部署关联
此配置文件会被通过 `docker-compose.yml` 挂载到 Nginx 容器的 `/etc/nginx/conf.d/default.conf` 位置，覆盖其默认配置。