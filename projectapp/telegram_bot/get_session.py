from telethon.sync import TelegramClient
from telethon.sessions import StringSession

api_id = 21825034
api_hash = "59915e8540fed369e2b1d633c1a7c82d"

with TelegramClient(StringSession(), api_id, api_hash) as client:
    print(client.session.save())
# gdfgdfgdfgdfg