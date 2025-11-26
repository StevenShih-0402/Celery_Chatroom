# 簡易聊天室專案

<嵌入 Youtube 影片：https://youtu.be/RHL5ABbohY8?si=mxGSWmQt-do3_rxC>

重點摘要：

1. 使用 Django 打造一個簡易聊天室介面與架構
2. 使用 Channels 套件建立 WebSocket 連線，支援多人即時聊天
3. 整合 Celery 處理背景任務，收集訊息到 Google Sheet，方便後續分析內容

目的：
紀錄從零開始建立 Django 專案，實作學習 WebSocket 連線與 Celery 背景任務處理。

前置作業：
1. 確保你的電腦有安裝 uv，若沒有安裝，請參考 uv 官方文件，或直接用以下指令安裝最新版 uv
2. 請先在你的雲端硬碟建立一份新的 Google Sheet 試算表，並開通 Google Sheet API 授權，可參考[此文章](https://hackmd.io/@StevenShih-0402/Hkk0xp0yWx)的"段落三、透過 Celery 收集留言內容"，
完成後應該會在專案放入一個 Google 金鑰檔案，將他改名為 creds.json。(若你想取其它名字，請同步修改 settings.py 的 GOOGLE_CREDS_PATH)

如何在本地啟動專案：
1. 在本地執行 `git clone https://github.com/StevenShih-0402/Celery_Chatroom.git`
2. 打開專案 (透過 Pycharm 或 VS Code)，執行 `uv sync` 同步依賴
3. 根據實際情況在 settings.py 修改 Google Sheet 設定
```python
# --- Google Sheet 設定 (請確保檔案存在) ---
GOOGLE_CREDS_PATH = BASE_DIR / 'creds.json'                         # 金鑰的路徑與檔案名稱
GOOGLE_SHEET_NAME = 'ChatLogs'                                      # 請確保你的 Google Sheet 有這個名稱的工作表
GOOGLE_SHEET_ID = '1XPTkoeddQmdh2YbxAZiYIKV-X1bBTVCJPBxEC39zPwU'    # Google Sheet 網址列中間的唯一代碼
```
4. 請將 settings.py 的設定進行調整，複製以下的 code 取代 "Channels & Redis 設定" 與 "Celery 設定"：
```python
# --- Channels & Redis 設定 ---
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

# --- Celery 設定 ---
CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_TASK_ALWAYS_EAGER = False # 確保任務真正進入佇列
```
4. 啟動兩個終端機：
- Daphne：`daphne project_chatroom.asgi:application -p 8000`
- Celery：`celery -A project_chatroom worker -l info -P solo`

如何在 Docker 啟動專案：
1. 在本地執行 `git clone https://github.com/StevenShih-0402/Celery_Chatroom.git`
2. 從終端機進入專案資料夾 (chatroom)，執行 `docker compose up --build -d`
3. 執行 docker compose ps，確認 Container 的運行狀態，確認 `chatroom_celery`、`chatroom_redis_app`、`chatroom_web` 三個映像檔的 STATUS 都是 up

啟動專案以後：
1. 在瀏覽器打開剛才建立的 Google Sheet 與另一個分頁，導向 `127.0.0.1:8000/chat`
2. 輸入聊天室名稱與用戶名稱，點選"進入"
3. 輸入訊息
4. 畫面與 Gooogle Sheet 應該就會看到內容有更新

開發過程分享：https://hackmd.io/@StevenShih-0402/Hkk0xp0yWx
