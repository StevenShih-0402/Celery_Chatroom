import os
from celery import Celery

# 設定 Django settings 模組
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_chatroom.settings')

app = Celery('project_chatroom')

# 從 settings.py讀取以 CELERY_ 開頭的配置
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自動發現各個 app 下的 tasks.py
app.autodiscover_tasks()