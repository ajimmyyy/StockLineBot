import os
from fastapi import FastAPI, Request, HTTPException
from linebot.v3 import (
    WebhookParser
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

from conversation import generate_reply

channel_secret = os.getenv('CHANNEL_SECRET', None)
channel_access_token = os.getenv('CHANNEL_ACCESS_TOKEN', None)

app = FastAPI()
configuration = Configuration(access_token=channel_access_token)
parser = WebhookParser(channel_secret)
line_bot_api = MessagingApi(ApiClient(configuration))

@app.post("/callback")
async def callback(request: Request):
    signature = request.headers['X-Line-Signature']
    body = await request.body()
    body = body.decode("utf-8")

    try:
        events = parser.parse(body, signature)
        for event in events:
            if not isinstance(event, MessageEvent):
                continue
            if not isinstance(event.message, TextMessageContent):
                continue
            reply_message = generate_reply(event.message.text)
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=reply_message)]
                )
            )
    except InvalidSignatureError:
        return HTTPException(status_code=400, detail='Invalid signature. Please check your channel access token/channel secret.')
    return 'OK'
