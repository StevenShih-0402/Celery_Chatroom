import json
from channels.generic.websocket import AsyncWebsocketConsumer
from datetime import datetime
# from .tasks import save_message_to_sheet # 即使註釋，也需要保留 import


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # 加入群組
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # 離開群組
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # 接收來自 WebSocket (前端) 的訊息
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json.get('username', 'Anonymous')

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 1. 呼叫 Celery Task (非同步寫入 Google Sheet)
        # save_message_to_sheet.apply_async(
        #     kwargs={
        #         "username": username,
        #         "message": message,
        #         "timestamp": now  # 確保鍵名與 tasks.py 裡的函數參數名稱一致
        #     }
        # )

        # 2. 廣播訊息給群組內的其他人
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'time': now
            }
        )

    # 接收來自群組的廣播
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        time = event['time']

        # 發送回 WebSocket (前端)
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'time': time
        }))