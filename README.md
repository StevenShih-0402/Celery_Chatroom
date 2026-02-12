<h1 align="center">🚀 Celery_Chatroom</h1>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?logo=python)](https://www.python.org/)
[![Framework: Django](https://img.shields.io/badge/Framework-Django-092E20.svg?logo=django)](https://www.djangoproject.com/)
[![Async: Channels](https://img.shields.io/badge/Async-Channels-ff69b4.svg)](https://channels.readthedocs.io/)
<br/>
[![Watch the DEMO video on YouTube](https://img.shields.io/badge/YouTube-操作範例影片-red?style=for-the-badge&logo=youtube)](https://youtu.be/RHL5ABbohY8?si=mxGSWmQt-do3_rxC)

## 🎯 專案簡介與目標

本專案是一個基於 Django 框架開發的簡易即時聊天室應用，專為演示和學習以下核心技術整合而設計：

* **Django Channels (WebSocket)：** 處理即時多人通訊。
* **Celery (背景任務)：** 處理非同步任務，如數據收集。
* **Redis：** 作為 Channels 的 Channel Layer 與 Celery 的 Broker/Backend。
* **Google Sheet API：** 將聊天記錄持久化到雲端試算表。

**核心價值：** 紀錄從零開始建立 Django 專案，實作學習 WebSocket 連線與 Celery 背景任務處理的完整流程。

---

## ✨ 功能與特性一覽

| 功能模組 | 說明 | 關鍵技術 |
| :--- | :--- | :--- |
| **即時通訊** | 建立多個獨立聊天室，支援多用戶即時訊息傳輸。 | Django Channels, WebSocket, Redis |
| **持久化數據收集** | 將聊天訊息 (時間戳、用戶、內容) 非同步寫入 Google Sheet。 | Celery, Google Sheet API |
| **可擴展架構** | 應用程式分為 ASGI 伺服器 (Daphne) 與 Worker (Celery)，可水平擴展。 | Daphne, Celery, Redis |

---

## 🛠️ 安裝與環境準備

在啟動專案之前，您需要準備以下工具並完成 Google Sheet 的授權設定。

### 步驟 A: 系統環境與工具

1.  **Git:** 用於複製專案。
2.  **uv:** 推薦的 Python 套件管理器。
3.  **Redis 服務:** 專案需要一個運行中的 Redis 實例（預設在 `127.0.0.1:6379`）。
    * **本地啟動適用：** 請確保您的本地環境已啟動 Redis Server。
    * **Docker 啟動適用：** Docker Compose 會自動啟動 Redis 容器。

### 步驟 B: Google Sheet API 設定

1.  **建立試算表：** 在 Google 雲端硬碟建立一份新的 Google Sheet。
2.  **開通 API 授權：** 執行 Google Sheet API 授權流程。
    > 📝 **參考資料：** 您可以參閱 [這篇文章的「段落三」](https://hackmd.io/@StevenShih-0402/Hkk0xp0yWx) 取得詳細步驟。
3.  **準備金鑰：** 將下載的 Google 服務帳戶金鑰檔案，更名為 `creds.json`，並放置於專案根目錄。

---

## ⚙️ 專案設定檔調整 (`settings.py`)

請進入專案根目錄，編輯 `project_chatroom/settings.py` 檔案：

### 1. Google Sheet 資訊

請將以下變數替換為您實際的 Google Sheet ID 和工作表名稱：

```python
# settings.py

# --- Google Sheet 設定 (請確保檔案存在) ---
GOOGLE_CREDS_PATH = BASE_DIR / 'creds.json'                             # 金鑰的路徑與檔案名稱
GOOGLE_SHEET_NAME = 'ChatLogs'                                          # 請確保你的 Google Sheet 有這個名稱的工作表
GOOGLE_SHEET_ID = '1XPTkoeddQmdh2YbxAZiYIKV-X1bBTVCJPBxEC39zPwU'        # Google Sheet 網址列中間的唯一代碼
```

### 2. Channels & Celery 連線

確認您的 Redis 連線配置為以下內容 (如果您的 Redis 服務不在 `127.0.0.1:6379`，請調整 `hosts`)：

```python
# settings.py

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
# ... (其他 Celery 設定保持不變)
```

## 💻 快速上手範例 (本地啟動)

### 1. 複製與安裝依賴

```bash
# 複製專案
git clone [https://github.com/StevenShih-0402/Celery_Chatroom.git](https://github.com/StevenShih-0402/Celery_Chatroom.git)
cd Celery_Chatroom

# 同步依賴
uv sync
```

### 2. 啟動服務 (三個終端機視窗)

請依序啟動以下三個必要服務：

| 服務 | 終端機指令 | 說明 |
| :--- | :--- | :--- |
| **Redis** | *[自行啟動您的 Redis Server]* | 訊息佇列與 Channel Layer 服務。 |
| **Daphne** | `daphne project_chatroom.asgi:application -p 8000` | ASGI 伺服器，處理 Web 頁面與 WebSocket 連線。 |
| **Celery** | `celery -A project_chatroom worker -l info -P solo` | 背景 Worker，處理寫入 Google Sheet 的非同步任務。 |

### 3. 執行與驗證

1.  開啟瀏覽器，導向 `http://127.0.0.1:8000/chat`。
2.  輸入聊天室名稱與用戶名稱，點選「進入」。
3.  發送訊息後，驗證訊息即時顯示在頁面，並檢查您的 **Google Sheet**，確認訊息已被成功記錄。

---

## 🐳 Docker 啟動 (一鍵部署)

若您偏好使用 Docker，專案已提供 `docker-compose.yml` 來一鍵啟動所有服務。

1.  **複製專案** (若尚未複製):
    ```bash
    git clone https://github.com/StevenShih-0402/Celery_Chatroom.git
    cd Celery_Chatroom
    ```

2.  **啟動容器：**
    ```bash
    docker compose up --build -d
    ```

3.  **驗證狀態：**
    ```bash
    docker compose ps
    ```
    (需確認 `chatroom_celery`, `chatroom_redis_app`, `chatroom_web` 狀態為 `up`)

4.  **訪問：** 瀏覽器導向 `http://127.0.0.1:8000/chat`。

---

## 📄 授權資訊

本專案採用 **MIT 授權條款**。詳情請見 [LICENSE](LICENSE) 檔案。

---

## 參考資料

* **完整開發過程分享：** [Django + Channels + Celery 打造即時聊天室 | Google Sheet 數據收集](https://hackmd.io/@StevenShih-0402/Hkk0xp0yWx)

