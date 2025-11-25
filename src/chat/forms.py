from django import forms

class MessageForm(forms.Form):
    # 定義訊息輸入欄位
    message = forms.CharField(
        label='',  # 聊天室通常不顯示 "Message" 這樣的標籤
        widget=forms.TextInput(attrs={
            'id': 'chat-message-input',      # 設定 ID 讓 JS 可以選取
            'placeholder': '傳送訊息...',     # 提示文字
            'autocomplete': 'off',           # 關閉瀏覽器自動完成
            # 為了配合 IG 風格，我們在這裡直接移除預設邊框
            'style': 'border: none; background: transparent; width: 100%; outline: none; font-size: 14px;'
        })
    )