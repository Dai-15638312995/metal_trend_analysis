# 使用官方 Python 3.10 镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 设置时区为 Asia/Shanghai
ENV TZ=Asia/Shanghai
ENV DEBIAN_FRONTEND=noninteractive

# 安装系统依赖（精简）
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        cron \
        tzdata \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir --disable-pip-version-check -r requirements.txt

# 复制项目文件
COPY . /app/

# 创建必要的目录
RUN mkdir -p /app/data/cache \
    /app/output/reports \
    /app/output/logs \
    /app/docker

# 设置脚本权限
RUN chmod +x /app/docker/entrypoint.sh

# 暴露端口（如果需要Web界面）
EXPOSE 8080

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# 默认命令：定时执行分析
CMD ["python", "src/main.py", "--instrument", "all"]
