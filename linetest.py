from flask import Flask
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    TextSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('hhIi5H7QMNVYu7k+h54mWfYbJHLHXNs9qaYHR3c6tXk2xPycF2SXDD0w/IkExcWQMLueuDi+XyuGFGLsLSRahzJ+o9WNec17WkGIYLlolwqu6X9PKzKpds6o6UTyxh9zqPSz+yiWcgQLEdP/QCyQGgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('942fda8d9642df31c76608b075a7ad43')


@app.route("/callback", methods=['POST', 'GET'])
def callback():
    line_bot_api.push_message('Uec530c8bc34ac510423bcfb5f2ee5711', TextSendMessage(text='Hello World!'))
    return 'ok'

if __name__ == "__main__":
    app.run(debug=True)