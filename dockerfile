FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制项目文件到工作目录
COPY . /app/

# 安装项目所需的依赖
RUN pip install -r requirements.txt

# 设置 Django 项目的环境变量
ENV DJANGO_SETTINGS_MODULE=server.settings

EXPOSE 5000
# 运行 Django 项目
CMD ["gunicorn", "server.wsgi:application", "--bind", "0.0.0.0:80"]
