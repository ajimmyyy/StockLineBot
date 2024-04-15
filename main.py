import os
import sys

import uvicorn

from langchain import hub
from langchain.memory import ConversationBufferWindowMemory
from langchain_openai import ChatOpenAI
from langchain.agents import (
    load_tools,
    create_openai_tools_agent,
    AgentExecutor,
    AgentType
)

from fastapi import Request, FastAPI, HTTPException
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

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('CHANNEL_SECRET', None)
channel_access_token = os.getenv('CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1) 

# create a FastAPI instance
app = FastAPI()
configuration = Configuration(access_token=channel_access_token)
parser = WebhookParser(channel_secret)
line_bot_api = MessagingApi(ApiClient(configuration))

# create a ChatOpenAI 
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# create an agent executor
prompt = hub.pull("hwchase17/openai-tools-agent")
memory = ConversationBufferWindowMemory(k=5)
tools = load_tools(["serpapi", "llm-math"], llm=llm)
agent = create_openai_tools_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, memory=memory, verbose=True)

# define a handler for the /callback endpoint
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

def generate_reply(input_text: str):
    response = agent_executor.invoke({"input": input_text})
    return response.get("output")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)