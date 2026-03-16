# =========================================================================
# 文件作用：后端项目 Docker 镜像构建脚本
# 构建步骤：准备 Python 运行环境，安装依赖，启动 FastAPI
# =========================================================================

# 使用官方 Python 3.10 轻量级镜像作为基础
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量：不生成 .pyc，且让输出直接打印不缓冲
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 更新 apt 并安装一些底层依赖 (如果处理复杂PDF需要额外的系统库，可以在此处安装)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖定义并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 复制全部后端代码
COPY . .

# 暴露 FastAPI 的默认端口
EXPOSE 8000

# 启动命令：使用 uvicorn 运行 main:app，绑定 0.0.0.0 和指定端口
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]