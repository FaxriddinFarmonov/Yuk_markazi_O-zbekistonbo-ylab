# # import asyncio
# # from telethon import TelegramClient, events
# #
# # # 🔑 3 ta akkaunt ma’lumotlari
# # accounts = [
# #     {
# #         "session": "acc1",
# #         "api_id": 21825034,
# #         "api_hash": "54914cdafa40fbb22d574799c0f38a9e",
# #         "source_groups": ["yuk_markazi_gruppaaaa", "yukmarkazi_isuzuchilar"]
# #     },
# #     {
# #         "session": "acc2",
# #         "api_id": 27622829,
# #         "api_hash": "070517eac99ddbdcbdbc6ef3113a120b",
# #         "source_groups": ["Yuk_markazi_yukmarkazi", "YUK_MARKAZI_XIZMATI"]
# #     },
# #     {
# #         "session": "acc3",
# #         "api_id": 28796243,
# #         "api_hash": "59915e8540fed369e2b1d633c1a7c82d",
# #         "source_groups": ["Surxondaryoyukmarkazi"]
# #     },
# # ]
# #
# # # 🏠 Forward qilinadigan guruh username
# # MY_GROUP = "yukmarkazi_isuzular"
# #
# # # ❌ Filtrlash uchun botlar / usernamelar
# # BLOCKED_SENDERS = ["Majbur_bot", "tg_botlar"]
# #
# #
# # async def run_client(account):
# #     client = TelegramClient(account["session"], account["api_id"], account["api_hash"])
# #
# #     await client.start()
# #     # 🔑 Guruhni entity sifatida olish
# #     my_group_entity = await client.get_entity(MY_GROUP)
# #
# #     @client.on(events.NewMessage(chats=account["source_groups"]))
# #     async def handler(event):
# #         sender = await event.get_sender()
# #         username = sender.username if sender else None
# #
# #         if username and username in BLOCKED_SENDERS:
# #             return
# #
# #         try:
# #             if event.raw_text:
# #                 await client.send_message(
# #                     my_group_entity,
# #                     f"{event.raw_text}\n\n👉 https://t.me/{MY_GROUP}"
# #                 )
# #                 print(f"[{account['session']}] Matn forward qilindi: {event.raw_text[:40]}")
# #             elif event.media:
# #                 await client.send_file(
# #                     my_group_entity,
# #                     event.media,
# #                     caption=f"👉 https://t.me/{MY_GROUP}"
# #                 )
# #                 # print(f"[{account['session']}] Media forward qilindi.")
# #         except Exception as e:
# #             print(f"[{account['session']}] ❌ Xabar yuborilmadi: {e}")
# #
# #     print(f"✅ {account['session']} ishga tushdi. Guruhlar: {account['source_groups']}")
# #     await client.run_until_disconnected()
# #
# #
# # async def main():
# #     tasks = [run_client(acc) for acc in accounts]
# #     await asyncio.gather(*tasks)
# #
# #
# # if __name__ == "__main__":
# #     print("🚀 Bot parallel ishlayapti...")
# #     asyncio.run(main())
# # # fgjhfggjfgjfjfgbdfbdfdx
#
#
#
# # forwarder_filtered.py
# import re
# import asyncio
# from telethon import TelegramClient, events
# from telethon.errors import FloodWaitError
#
# # --------------------
# # 3 ta akkaunt + ularning guruhlari
# accounts = [
#     {
#         "session": "acc1",
#         "api_id": 21825034,
#         "api_hash": "54914cdafa40fbb22d574799c0f38a9e",
#         "source_groups": ["yuk_markazi_gruppaaaa", "yukmarkazi_isuzuchilar"]
#     },
#     {
#         "session": "acc2",
#         "api_id": 27622829,
#         "api_hash": "070517eac99ddbdcbdbc6ef3113a120b",
#         "source_groups": ["Yuk_markazi_yukmarkazi", "YUK_MARKAZI_XIZMATI"]
#     },
#     {
#         "session": "acc3",
#         "api_id": 28796243,
#         "api_hash": "59915e8540fed369e2b1d633c1a7c82d",
#         "source_groups": ["Surxondaryoyukmarkazi", "yuk_markazi_vodiy_yuk_markazi"]
#     },
# ]
#
# # Forward qilinadigan guruh (username)
# MY_GROUP = "yukmarkazi_isuzular"
#
# # Keraksiz yuboruvchilar / botlar
# BLOCKED_SENDERS = {"Majbur_bot", "tg_botlar"}
#
# # Nomaqbul so'zlar (kichik harfga o'girib tekshiriladi)
# BANNED_WORDS = [
#     "sex", "seks", "online kayf", "porno", "escort", "seks", "erotic", "yopildi",
#     "licga", "lic", "kayf", "seks", "mast", "trav", "escort"
# ]
#
# # Telefon raqamni aniqlovchi regexlar (bularni tarzda kengaytirish mumkin)
# PHONE_REGEX = re.compile(
#     r"(\+998\d{9}|\+7\d{10}|\+\d{6,15}|\b0\d{8,10}\b)"
#     , flags=re.IGNORECASE
# )
#
# # Kanal/kanal-preview yoki "VIEW GROUP" kabi avtomatik bloklovchi so'zlar
# BLOCK_PREVIEWS = ["view group", "view channel", "telegram", "view group", "view channel"]
#
# # Delay har bir forwarddan keyin (sekund)
# AFTER_FORWARD_DELAY = 2
#
# # --------------------
# def text_has_phone(text: str) -> bool:
#     if not text:
#         return False
#     return bool(PHONE_REGEX.search(text))
#
#
# def text_has_banned_word(text: str) -> bool:
#     if not text:
#         return False
#     s = text.lower()
#     for w in BANNED_WORDS:
#         if w in s:
#             return True
#     for p in BLOCK_PREVIEWS:
#         if p in s:
#             return True
#     # Shuningdek, agar link preview (masalan "VIEW GROUP") yoki kanal tavsifi bo'lsa
#     if "view group" in s or "view channel" in s:
#         return True
#     return False
#
#
# async def run_client(account):
#     client = TelegramClient(account["session"], account["api_id"], account["api_hash"])
#     await client.start()
#     # Entity sifatida MY_GROUP ni oling (username orqali)
#     try:
#         my_group_entity = await client.get_entity(MY_GROUP)
#     except Exception as e:
#         print(f"[{account['session']}] MY_GROUP entity olinmadi: {e}")
#         my_group_entity = MY_GROUP  # fallback: username bilan ishlatamiz
#
#     source_groups = account.get("source_groups", [])
#     print(f"[{account['session']}] ishga tushdi. Kuzatiladi: {source_groups}")
#
#     @client.on(events.NewMessage(chats=source_groups))
#     async def handler(event):
#         try:
#             # chat haqida ma'lumot
#             try:
#                 chat = await event.get_chat()
#                 chat_title = getattr(chat, "title", None) or getattr(chat, "username", str(event.chat_id))
#             except:
#                 chat_title = str(event.chat_id)
#
#             sender = await event.get_sender()
#             sender_name = (sender.username if sender and sender.username else
#                            (getattr(sender, "first_name", None) or str(getattr(sender, "id", "unknown"))))
#
#             # Agar yuboruvchi block ro'yxatda bo'lsa — o'tkazmaslik
#             if sender and getattr(sender, "username", None) in BLOCKED_SENDERS:
#                 # log uchun
#                 print(f"[{account['session']}] BLOCKED sender {sender.username} dan xabar tashlanmadi.")
#                 return
#
#             text = event.raw_text or ""
#             # Agar matn yoki caption yo'q va media ham bo'lsa — media bilan qayta ishlaymiz,
#             # lekin telefonsiz media yuborish shart emas (siz telefonsiz media ham olishni xohlamadingiz)
#             # Shuning uchun media bo'lsa va captionda telefon bo'lsa forward qilamiz
#             has_phone = text_has_phone(text)
#
#             # Agar matnda nomaqbul so'zlar bo'lsa — tashlamaymiz
#             if text_has_banned_word(text):
#                 print(f"[{account['session']}] {chat_title} dan nomaqbul xabar topildi — tashlanmadi.")
#                 return
#
#             # Agar telefon raqami yo'q bo'lsa — tashlamaymiz
#             if not has_phone:
#                 # Agar media va caption mavjud bo'lsa, captionni tekshiramiz
#                 cap = getattr(event.message, "message", "") or ""
#                 if text_has_phone(cap):
#                     has_phone = True
#                 else:
#                     # Ba'zi hollarda xabar ichida alohida entity (phone) bo'lishi mumkin - qo'shimcha tekshir
#                     if not has_phone:
#                         print(f"[{account['session']}] {chat_title} dan xabar TOPILMADI (telefon yo'q) — tashlanmadi.")
#                         return
#
#             # Endi forward/forward-like yuborish
#             try:
#                 # Forward qilish (asl yuboruvchini saqlab qoladi)
#                 # event.forward_to(my_group_entity)  # forward_to ni ishlatish mumkin, lekin ba'zan kerakli caption qo'shish qiyin
#                 # Biz original matnni yangi xabar sifatida yuboramiz + link qo'shamiz
#                 if text:
#                     send_text = f"{text}\n\n📌 Manba: {chat_title}\n📨 Yuborgan: {sender_name}\n\n👉 https://t.me/{MY_GROUP}"
#                     await client.send_message(my_group_entity, send_text)
#                 elif event.media:
#                     # agar media bo'lsa, avval media yuklab yuborib caption bilan
#                     caption = f"📌 Manba: {chat_title}\n📨 Yuborgan: {sender_name}\n\n👉 https://t.me/{MY_GROUP}"
#                     await client.send_file(my_group_entity, event.media, caption=caption)
#
#                 print(f"[{account['session']}] ✅ {chat_title} dan {sender_name} dan xabar saqlandi va yuborildi.")
#                 await asyncio.sleep(AFTER_FORWARD_DELAY)
#
#             except FloodWaitError as e:
#                 print(f"[{account['session']}] FloodWait: {e.seconds}s kutilyapti...")
#                 await asyncio.sleep(e.seconds + 1)
#
#         except Exception as exc:
#             print(f"[{account['session']}] Handler xatosi: {exc}")
#
#     await client.run_until_disconnected()
#
#
# async def main():
#     tasks = [run_client(acc) for acc in accounts]
#     await asyncio.gather(*tasks)
#
#
# if __name__ == "__main__":
#     print("▶️ Forwarder ishga tushmoqda...")
#     asyncio.run(main())


#
# import asyncio
# from telethon import TelegramClient, events
# from telethon.errors import FloodWaitError
#
# # --------------------
# # 3 ta akkaunt + ularning guruhlari
# accounts = [
#     {
#         "session": "acc1",
#         "api_id": 21825034,
#         "api_hash": "54914cdafa40fbb22d574799c0f38a9e",
#         "source_groups": ["yuk_markazi_gruppaaaa", "yukmarkazi_isuzuchilar"]
#     },
#     {
#         "session": "acc2",
#         "api_id": 27622829,
#         "api_hash": "070517eac99ddbdcbdbc6ef3113a120b",
#         "source_groups": ["Yuk_markazi_yukmarkazi", "YUK_MARKAZI_XIZMATI"]
#     },
#     {
#         "session": "acc3",
#         "api_id": 28796243,
#         "api_hash": "59915e8540fed369e2b1d633c1a7c82d",
#         "source_groups": ["Surxondaryoyukmarkazi", "yuk_markazi_vodiy_yuk_markazi"]
#     },
# ]
#
# # Forward qilinadigan guruh (username)
# MY_GROUP = "yukmarkazi_isuzular"
#
# # Keraksiz yuboruvchilar / botlar
# BLOCKED_SENDERS = {"Majbur_bot", "tg_botlar"}
#
# # Delay har bir forwarddan keyin (sekund)
# AFTER_FORWARD_DELAY = 2
#
#
# async def run_client(account):
#     client = TelegramClient(account["session"], account["api_id"], account["api_hash"])
#     await client.start()
#
#     # Entity sifatida MY_GROUP ni olish
#     try:
#         my_group_entity = await client.get_entity(MY_GROUP)
#     except Exception as e:
#         print(f"[{account['session']}] MY_GROUP entity olinmadi: {e}")
#         my_group_entity = MY_GROUP
#
#     source_groups = account.get("source_groups", [])
#     print(f"[{account['session']}] ishga tushdi. Kuzatiladi: {source_groups}")
#
#     @client.on(events.NewMessage(chats=source_groups))
#     async def handler(event):
#         try:
#             sender = await event.get_sender()
#             sender_name = sender.username if sender and sender.username else "unknown"
#
#             # Agar yuboruvchi block ro'yxatda bo'lsa — o'tkazmaslik
#             if sender_name in BLOCKED_SENDERS:
#                 print(f"[{account['session']}] BLOCKED sender {sender_name} dan xabar tashlanmadi.")
#                 return
#
#             # Endi forward qilish
#             try:
#                 if event.raw_text:
#                     await client.send_message(my_group_entity, event.raw_text)
#                 elif event.media:
#                     await client.send_file(my_group_entity, event.media, caption=event.message.message or "")
#
#                 print(f"[{account['session']}] ✅ Xabar yuborildi ({sender_name}).")
#                 await asyncio.sleep(AFTER_FORWARD_DELAY)
#
#             except FloodWaitError as e:
#                 print(f"[{account['session']}] FloodWait: {e.seconds}s kutilyapti...")
#                 await asyncio.sleep(e.seconds + 1)
#
#         except Exception as exc:
#             print(f"[{account['session']}] Handler xatosi: {exc}")
#
#     await client.run_until_disconnected()
#
#
# async def main():
#     tasks = [run_client(acc) for acc in accounts]
#     await asyncio.gather(*tasks)
#
#
# if __name__ == "__main__":
#     print("▶️ Forwarder ishga tushmoqda...")
#     asyncio.run(main())


import asyncio
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError

# --------------------
# 3 ta akkaunt + ularning guruhlari
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
        "source_groups": ["Surxondaryoyukmarkazi", "yuk_markazi_vodiy_yuk_markazi"]
    },
]

# Forward qilinadigan guruh (username)
MY_GROUP = "yukmarkazi_isuzular"

# Keraksiz yuboruvchilar / botlar
BLOCKED_SENDERS = {"Majbur_bot", "tg_botlar"}

# Delay har bir forwarddan keyin (sekund)
AFTER_FORWARD_DELAY = 2


async def run_client(account):
    client = TelegramClient(account["session"], account["api_id"], account["api_hash"])
    await client.start()

    # Entity sifatida MY_GROUP ni olish
    try:
        my_group_entity = await client.get_entity(MY_GROUP)
    except Exception as e:
        print(f"[{account['session']}] MY_GROUP entity olinmadi: {e}")
        my_group_entity = MY_GROUP

    source_groups = account.get("source_groups", [])
    print(f"[{account['session']}] ishga tushdi. Kuzatiladi: {source_groups}")

    @client.on(events.NewMessage(chats=source_groups))
    async def handler(event):
        try:
            sender = await event.get_sender()
            sender_name = sender.username if sender and sender.username else "unknown"

            # Agar yuboruvchi block ro'yxatda bo'lsa — o'tkazmaslik
            if sender_name in BLOCKED_SENDERS:
                print(f"[{account['session']}] BLOCKED sender {sender_name} dan xabar tashlanmadi.")
                return

            # ❌ Media (rasm, video, fayl) tashlanmasin
            if event.media:
                print(f"[{account['session']}] ❌ Media xabar tashlanmadi ({sender_name}).")
                return

            # Endi faqat text forward qilamiz
            if event.raw_text:
                send_text = f"{event.raw_text}\n\n📨 Yuborgan: {sender_name}\n\n👉 https://t.me/{MY_GROUP}"
                await client.send_message(my_group_entity, send_text)
                print(f"[{account['session']}] ✅ Matn yuborildi ({sender_name}).")

            await asyncio.sleep(AFTER_FORWARD_DELAY)

        except FloodWaitError as e:
            print(f"[{account['session']}] FloodWait: {e.seconds}s kutilyapti...")
            await asyncio.sleep(e.seconds + 1)

        except Exception as exc:
            print(f"[{account['session']}] Handler xatosi: {exc}")

    await client.run_until_disconnected()


async def main():
    tasks = [run_client(acc) for acc in accounts]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    print("▶️ Forwarder ishga tushmoqda...")
    asyncio.run(main())
