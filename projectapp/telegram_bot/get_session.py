from telethon.sync import TelegramClient
from telethon.sessions import StringSession

api_id = 21825034
api_hash = "54914cdafa40fbb22d574799c0f38a9e"

with TelegramClient(StringSession(), api_id, api_hash) as client:
    print(client.session.save())
