from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage   # 載入 TextSendMessage 模組
import json
from AI_assisant import chat
from dotenv import load_dotenv
import os

# 載入環境變數
load_dotenv()

app = Flask(__name__)

# 從環境變數獲取設定
CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")
CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")

@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)
    json_data = json.loads(body)
    print(json_data)
    try:
        line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
        handler = WebhookHandler(CHANNEL_SECRET)
        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)
        tk = json_data['events'][0]['replyToken']         # 取得 reply token
        msg = json_data['events'][0]['message']['text']   # 取得使用者發送的訊息
        text_message = TextSendMessage(text = chat(msg))  # 設定回傳同樣的訊息
        # text_message = TextSendMessage(text=msg)          # 設定回傳同樣的訊息

        line_bot_api.reply_message(tk,text_message)       # 回傳訊息
    except Exception as e:
        print('error: ' + str(e))
    return 'OK'

app.run(port="5000")
