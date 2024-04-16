# main.py
import os
import sys
import uvicorn

from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

channel_secret = os.getenv('CHANNEL_SECRET', None)
channel_access_token = os.getenv('CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
