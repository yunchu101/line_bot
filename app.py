from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('PndIofrjGPcQCm6p9p6kYK5s8y8+z2cl6/Ycn7dUs2JML3S1V2PtMxVlwpZLpW+VTliG1atMTys3Ty5ezclT86zdi49QcRp1oCgSsBbupvoBEjh8gxC+JxQ4jm6eXWw3BnkM6v2uuNPDsQZ0nzPsZgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('f8b743bb0288cef2530665373330769e')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()