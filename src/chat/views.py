from django.shortcuts import render
from .forms import MessageForm  # 引入剛剛建立的 Form


def index(request):
    return render(request, 'chat/index.html')


def room(request, room_name):
    # 從 URL GET 參數獲取使用者名稱，預設為 'Guest' (例如 ?username=ChromeUser)
    username = request.GET.get('username', 'Guest')

    # 實例化表單
    form = MessageForm()

    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'username': username,
        'form': form  # 將表單物件傳遞給前端 Template
    })
