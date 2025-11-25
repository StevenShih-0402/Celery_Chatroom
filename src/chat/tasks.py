import gspread
from celery import shared_task
from django.conf import settings
from oauth2client.service_account import ServiceAccountCredentials


@shared_task
def save_message_to_sheet(username, message, timestamp):
    """
    這個任務會在背景執行，負責連線 Google Sheet 並寫入資料。
    """
    try:
        # 檢查憑證是否存在 (避免開發時報錯)
        if not settings.GOOGLE_CREDS_PATH.exists():
            print(f"[Celery] 找不到 creds.json，跳過寫入。內容: {username}: {message}")
            return

        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(settings.GOOGLE_CREDS_PATH, scope)
        client = gspread.authorize(creds)

        # 開啟試算表
        sheet = client.open(settings.GOOGLE_SHEET_NAME).sheet1

        # 寫入一行: [時間, 使用者, 訊息]
        sheet.append_row([timestamp, username, message])
        print(f"[Celery] 成功寫入: {message}")

    except Exception as e:
        print(f"[Celery Error] 寫入 Google Sheet 失敗: {e}")