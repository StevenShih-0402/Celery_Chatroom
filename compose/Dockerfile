# 使用 Python 3.11 官方輕量級映象檔作為基礎
FROM python:3.11-slim

# 設定 Django 環境變數
# 1. stdout/stderr 不使用緩衝，直接輸出到 console。
# 2. 設定 Django 的 settings 路徑
# 3. uv 的設定，控制套件安裝時的「link mode」。
# 4. 設定容器的語言與編碼環境為 UTF-8。
ENV PYTHONUNBUFFERED 1 \
    DJANGO_SETTINGS_MODULE project_chatroom.settings \
    UV_LINK_MODE=copy \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

# 安裝基礎開發工具與憑證
# 更新 apt 套件索引清單
# 安裝 Git，為了 clone 自己修改的套件
# 只安裝明確指定的套件，即使有相關的套件也不安裝 (減少映像檔體積)
# 安裝完成後清除快取
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl gcc python3-dev build-essential locales \
    && locale-gen C.UTF-8 \
    && rm -rf /var/lib/apt/lists/*

# 安裝最新版 uv
RUN curl -fsSL https://astral.sh/uv/install.sh | sh \
    && ln -s /root/.local/bin/uv /usr/local/bin/uv

# 掛載程式碼的位址 (應與 docker-compose 的 volumes 一樣)
WORKDIR /var/www/html/

# 將專案依賴文件 (pyproject.toml 和 uv.lock) 複製到容器中
COPY pyproject.toml ./
COPY uv.lock ./

# 安裝 pyproject.toml 的依賴
RUN uv pip install --requirements pyproject.toml --system

# 容器預設暴露 8000 埠 (用於 Daphne)
EXPOSE 8000