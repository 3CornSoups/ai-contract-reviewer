# =========================================================================
# 文件作用：前端项目 Docker 镜像构建脚本
# 构建步骤：基于 Node 编译，产物拷贝到 Nginx 镜像中进行部署
# =========================================================================

# 第一阶段：构建依赖与编译产物
# 选择包含 npm 的轻量基础镜像
FROM node:18-alpine AS builder

WORKDIR /app

# 优先拷贝 package.json 利用 Docker 缓存机制加速 npm install
COPY package*.json ./
RUN npm install --registry=https://registry.npmmirror.com/

# 拷贝源代码并执行生产环境构建
COPY . .
RUN npm run build

# 第二阶段：生产环境运行
# 选用 Nginx 轻量镜像作为最终运行时
FROM nginx:alpine

# 将构建好的前端 dist 产物拷贝到 Nginx 的默认静态资源目录
COPY --from=builder /app/dist /usr/share/nginx/html

# 覆盖 Nginx 的默认配置 (注意：我们会在 docker-compose.yml 中通过 volume 将外部 nginx.conf 挂载进来，此处可选，为保证独立运行也可在此拷贝)
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# 暴露 80 端口
EXPOSE 80

# 启动 Nginx
CMD ["nginx", "-g", "daemon off;"]