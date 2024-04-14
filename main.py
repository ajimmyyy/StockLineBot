import os
import sys

import uvicorn
import aiohttp

from langchain_openai import ChatOpenAI

from fastapi import Request, FastAPI, HTTPException
from linebot import AsyncLineBotApi, WebhookParser

from linebot.aiohttp_async_http_client import AiohttpAsyncHttpClient
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('CHANNEL_SECRET', None)
channel_access_token = os.getenv('CHANNEL_ACCESS_TOKEN', None)
openai_api_key = os.getenv('OPENAI_API_KEY', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)
if openai_api_key is None:
    print('Specify OPENAI_API_KEY as environment variable.')
    sys.exit(1)

# create a FastAPI instance
app = FastAPI()
session = aiohttp.ClientSession()
async_http_client = AiohttpAsyncHttpClient(session)
line_bot_api = AsyncLineBotApi(channel_access_token, async_http_client)
parser = WebhookParser(channel_secret)

# create a ChatOpenAI instance
chat = ChatOpenAI(model="gpt-3.5-turbo", api_key=openai_api_key)

# define a handler for the /callback endpoint
@app.post("/callback")
async def callback(request: Request):
    signature = request.headers['X-Line-Signature']
    body = await request.body()
    body = body.decode('utf-8')

    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        return HTTPException(status_code=400, detail='Invalid signature. Please check your channel access token/channel secret.')

    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        user_message = event.message.text
        response = chat.invoke(user_message)
        reply_message = TextSendMessage(text=response)
        await line_bot_api.reply_message(event.reply_token, reply_message)

    return 'OK'

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)