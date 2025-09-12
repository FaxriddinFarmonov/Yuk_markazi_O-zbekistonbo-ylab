import asyncio
from telethon import TelegramClient, events

# 3 ta akkaunt + ularning guruhlari
accounts = [
    {"session": "acc1", "api_id": 21825034, "api_hash": "54914cdafa40fbb22d574799c0f38a9e", "groups": ["yuk_markazi_gruppaaaa"]},
    {"session": "acc2", "api_id": 27622829, "api_hash": "070517eac99ddbdcbdbc6ef3113a120b", "groups": ["yukmarkazi_isuzuchilar"]},
    {"session": "acc3", "api_id": 28796243, "api_hash": "59915e8540fed369e2b1d633c1a7c82d", "groups": ["Surxondaryoyukmarkazi"]},
]

MY_GROUP = "yukmarkazi_isuzular"
BLOCKED_SENDERS = ["Majbur_bot", "tg_botlar"]

def setup_handlers(client, groups):
    @client.on(events.NewMessage(chats=groups))
    async def handler(event):
        sender = await event.get_sender()
        username = sender.username if sender else None
        if username and username in BLOCKED_SENDERS:
            return
        try:
            if event.raw_text:
                await client.send_message(MY_GROUP, f"{event.raw_text}\n\n👉 https://t.me/{MY_GROUP}")
            elif event.media:
                await client.send_file(MY_GROUP, event.media, caption=f"👉 https://t.me/{MY_GROUP}")
            print(f"✅ {username or sender.id} dan xabar ko‘chirildi.")
            await asyncio.sleep(2)
        except Exception as e:
            print(f"❌ Xatolik: {e}")

async def start_client(acc):
    client = TelegramClient(acc["session"], acc["api_id"], acc["api_hash"])
    await client.start()
    setup_handlers(client, acc["groups"])
    print(f"🚀 {acc['session']} ishga tushdi... (gruppalar: {acc['groups']})")
    # run_until_disconnected alohida task sifatida
    await client.run_until_disconnected()

async def main():
    print("🔥 Barcha akkauntlar parallel ishlamoqda...")
    # Har bir clientni alohida task sifatida ishga tushiramiz
    tasks = [asyncio.create_task(start_client(acc)) for acc in accounts]
    # Barcha tasklarni kutamiz
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
