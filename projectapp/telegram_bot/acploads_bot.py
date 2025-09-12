import asyncio
from telethon import TelegramClient, events

# 🔑 3 ta akkaunt ma’lumotlari
accounts = [
    {
        "session": "acc1",
        "api_id": 21825034,
        "api_hash": "54914cdafa40fbb22d574799c0f38a9e",
        "source_groups": ["yuk_markazi_gruppaaaa", "yukmarkazi_isuzuchilar"]
    },
    {
        "session": "acc2",
        "api_id": 27622829,
        "api_hash": "070517eac99ddbdcbdbc6ef3113a120b",
        "source_groups": ["Yuk_markazi_yukmarkazi", "YUK_MARKAZI_XIZMATI"]
    },
    {
        "session": "acc3",
        "api_id": 28796243,
        "api_hash": "59915e8540fed369e2b1d633c1a7c82d",
        "source_groups": ["Surxondaryoyukmarkazi"]
    },
]

# 🏠 Forward qilinadigan guruh username
MY_GROUP = "yukmarkazi_isuzular"

# ❌ Filtrlash uchun botlar / usernamelar
BLOCKED_SENDERS = ["Majbur_bot", "tg_botlar"]


async def run_client(account):
    client = TelegramClient(account["session"], account["api_id"], account["api_hash"])

    await client.start()
    # 🔑 Guruhni entity sifatida olish
    my_group_entity = await client.get_entity(MY_GROUP)

    @client.on(events.NewMessage(chats=account["source_groups"]))
    async def handler(event):
        sender = await event.get_sender()
        username = sender.username if sender else None

        if username and username in BLOCKED_SENDERS:
            return

        try:
            if event.raw_text:
                await client.send_message(
                    my_group_entity,
                    f"{event.raw_text}\n\n👉 https://t.me/{MY_GROUP}"
                )
                print(f"[{account['session']}] Matn forward qilindi: {event.raw_text[:40]}")
            elif event.media:
                await client.send_file(
                    my_group_entity,
                    event.media,
                    caption=f"👉 https://t.me/{MY_GROUP}"
                )
                print(f"[{account['session']}] Media forward qilindi.")
        except Exception as e:
            print(f"[{account['session']}] ❌ Xabar yuborilmadi: {e}")

    print(f"✅ {account['session']} ishga tushdi. Guruhlar: {account['source_groups']}")
    await client.run_until_disconnected()


async def main():
    tasks = [run_client(acc) for acc in accounts]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    print("🚀 Bot parallel ishlayapti...")
    asyncio.run(main())
# fgjhfggjfgjfjfgbdfbdfdx