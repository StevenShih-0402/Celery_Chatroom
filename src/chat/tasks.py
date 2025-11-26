from project_chatroom.celery import app  # 引入 Celery 實例
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError  # ★ 新增：引入 Google API Client 的錯誤類型
from django.conf import settings
import logging
import os
import gspread  # 引入 gspread 以便於使用它的錯誤處理或功能 (但實際 API 呼叫使用的是 googleapiclient)

logger = logging.getLogger(__name__)

# Google Sheet API 範圍
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


@app.task(bind=True)
def save_message_to_sheet(self, room_name, username, message, timestamp):
    """
    將聊天訊息寫入 Google Sheet 的 Celery 任務。
    此任務在背景執行，以避免阻塞主 Web 服務。
    """
    try:
        # 1. 驗證金鑰路徑是否存在
        creds_path = settings.GOOGLE_CREDS_PATH
        if not os.path.exists(creds_path):
            logger.error(f"Google 服務帳戶金鑰未找到於: {creds_path}。請參閱指引文件。")
            return

        # 2. 載入憑證
        creds = Credentials.from_service_account_file(creds_path, scopes=SCOPES)

        # 3. 建立 Google Sheets API 服務 (使用 googleapiclient)
        service = build('sheets', 'v4', credentials=creds)

        # 4. 準備寫入資料
        data_to_write = [[
            str(timestamp),  # 確保時間戳記為字串格式
            room_name,
            username,
            message
        ]]

        # 5. 獲取試算表 ID 和名稱
        sheet_id = settings.GOOGLE_SHEET_ID  # 從 settings.py 中獲取
        sheet_name = settings.GOOGLE_SHEET_NAME  # 從 settings.py 中獲取

        # 6. 執行寫入操作 (使用 append 方式，從下一行開始寫入)
        logger.info(f"嘗試寫入訊息到 Google Sheet ID: {sheet_id}, Sheet: {sheet_name}")

        result = service.spreadsheets().values().append(
            spreadsheetId=sheet_id,
            # 寫入範圍。這裡使用 'A:D' 假設您的資料欄位是 A 到 D
            range=f"{sheet_name}!A:D",
            valueInputOption="USER_ENTERED",
            body={'values': data_to_write}
        ).execute()

        update_range = result.get('updates').get('updatedRange')
        logger.info(f"Celery 任務成功寫入 Google Sheet: {update_range}")

    except HttpError as e:  # ★ 修正：只捕捉 googleapiclient 拋出的 HttpError
        # 400 (Bad Request - 範圍錯誤) 或 403 (權限不足)
        # 這裡會捕捉到 "Unable to parse range" 錯誤 (400)
        logger.error(f"寫入 Google Sheet 發生 API 錯誤 ({e.resp.status}): {e.content.decode()}")

        # 只有在可能是暫時性問題時才重試 (例如：500/503 伺服器錯誤)
        if e.resp.status in (500, 503):
            logger.error("API 伺服器暫時性錯誤，嘗試重試...")
            raise self.retry(exc=e, countdown=15, max_retries=3)

        # 對於 400 (範圍錯誤) 或 403 (權限錯誤)，不重試，因為問題在配置
        pass  # 讓任務失敗

    except Exception as e:
        # 捕捉其他所有未預期的錯誤
        logger.critical(f"寫入 Google Sheet 發生未預期的嚴重錯誤: {e}")
        # 不需要 self.retry()，直接讓任務失敗