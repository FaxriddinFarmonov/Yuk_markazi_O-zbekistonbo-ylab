

# # optimized_forwarder_with_source_log.py
# import asyncio
# import sqlite3
# import time
# import random
# from telethon import TelegramClient, events
# from telethon.errors import FloodWaitError, RPCError
#
# accounts = [
#     {"session": "acc1", "api_id": 21825034, "api_hash": "54914cdafa40f...", "source_groups": ["yuk_markazi_gruppaaaa","YUK_MARKAZI_XIZMATI"]},
#     {"session": "acc2", "api_id": 27622829, "api_hash": "070517eac99d...", "source_groups": ["Yuk_markazi_yukmarkazi","lorry_uzbek"]},  # <-- note: no /1
#     {"session": "acc3", "api_id": 28796243, "api_hash": "59915e8540fe...", "source_groups": ["Surxondaryoyukmarkazi", "yukmarkazi_isuzuchilar"]},
# ]
#
# MY_GROUP = "yukmarkazi_isuzular"
# BLOCKED_SENDERS = {"Majbur_bot", "tg_botlar"}
#
# account_semaphores = {}
# DB_FILE = "forwarder.db"
# conn = sqlite3.connect(DB_FILE, check_same_thread=False)
# cur = conn.cursor()
# cur.execute('''
# CREATE TABLE IF NOT EXISTS messages (
#   id INTEGER PRIMARY KEY AUTOINCREMENT,
#   chat_id TEXT,
#   msg_id TEXT,
#   sender TEXT,
#   text TEXT,
#   media INTEGER DEFAULT 0,
#   forwarded INTEGER DEFAULT 0,
#   created_at REAL
# )
# ''')
# conn.commit()
#
# async def retry_with_backoff(coro_func, *args, max_tries=5, base=1.5):
#     tries = 0
#     while tries < max_tries:
#         try:
#             return await coro_func(*args)
#         except FloodWaitError as e:
#             wait = e.seconds + 1
#             print(f"[retry] FloodWaitError: kutilyapti {wait}s")
#             await asyncio.sleep(wait)
#         except RPCError as e:
#             tries += 1
#             wait = base ** tries + random.random()
#             print(f"[retry] RPCError ({e}). kutilyapti {wait:.1f}s, urinish {tries}/{max_tries}")
#             await asyncio.sleep(wait)
#         except Exception as e:
#             tries += 1
#             wait = base ** tries + random.random()
#             print(f"[retry] Other error ({e}). kutilyapti {wait:.1f}s, urinish {tries}/{max_tries}")
#             await asyncio.sleep(wait)
#     raise RuntimeError("Max retry attempts reached")
#
# async def forward_message(client, my_group_entity, event, account_name):
#     # Get chat info (Manba) and sender
#     try:
#         chat = await event.get_chat()
#         chat_title = getattr(chat, "title", None) or getattr(chat, "username", None) or str(event.chat_id)
#     except:
#         chat_title = str(event.chat_id)
#
#     try:
#         sender = await event.get_sender()
#         sender_name = sender.username if sender and getattr(sender, "username", None) else (getattr(sender, "first_name", "unknown") or str(getattr(sender, "id", "unknown")))
#     except:
#         sender_name = "unknown"
#
#     text = event.raw_text or ""
#     media_flag = 1 if event.media else 0
#
#     cur.execute(
#         "INSERT INTO messages (chat_id, msg_id, sender, text, media, forwarded, created_at) VALUES (?,?,?,?,?,?,?)",
#         (str(event.chat_id), str(getattr(event.message, 'id', '')), sender_name, text, media_flag, 0, time.time())
#     )
#     conn.commit()
#     msg_db_id = cur.lastrowid
#
#     # Log source (manba)
#     print(f"[{account_name}] Manba: {chat_title} | Yuborgan: {sender_name} | Text len: {len(text)}")
#
#     sem = account_semaphores[account_name]
#     async with sem:
#         async def do_forward():
#             try:
#                 await event.forward_to(my_group_entity)
#                 return "forwarded"
#             except Exception:
#                 if event.raw_text:
#                     await client.send_message(my_group_entity, event.raw_text)
#                     return "sent_text"
#                 else:
#                     raise
#
#         result = await retry_with_backoff(do_forward)
#         cur.execute("UPDATE messages SET forwarded=1 WHERE id=?", (msg_db_id,))
#         conn.commit()
#         print(f"[{account_name}] {result} ({chat_title} -> {MY_GROUP})")
#
# async def run_client(account):
#     name = account["session"]
#     account_semaphores[name] = asyncio.Semaphore(1)
#     client = TelegramClient(name, account["api_id"], account["api_hash"])
#
#     await client.start()
#     try:
#         my_group_entity = await client.get_entity(MY_GROUP)
#     except Exception as e:
#         print(f"[{name}] MY_GROUP olinmadi: {e}; fallback to username")
#         my_group_entity = MY_GROUP
#
#     groups = account.get("source_groups", [])
#     print(f"[{name}] ishga tushdi. Kuzatiladi: {groups}")
#
#     @client.on(events.NewMessage(chats=groups))
#     async def handler(event):
#         # blocked senders
#         try:
#             sender = await event.get_sender()
#             if sender and getattr(sender, "username", None) in BLOCKED_SENDERS:
#                 print(f"[{name}] BLOCKED sender {sender.username}")
#                 return
#         except:
#             pass
#
#         # skip media if you don't want them
#         if event.media:
#             print(f"[{name}] media skipped")
#             return
#
#         # start forwarding task immediately
#         asyncio.create_task(forward_message(client, my_group_entity, event, name))
#
#     await client.run_until_disconnected()
#
# async def main():
#     tasks = [run_client(acc) for acc in accounts]
#     await asyncio.gather(*tasks)
#
# if __name__ == "__main__":
#     print("▶️ Optimized forwarder starting...")
#     asyncio.run(main())


import asyncio
import random
import re
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError, RPCError

accounts = [
    {"session": "acc1", "api_id": 21825034, "api_hash": "54914cdafa40f...", "source_groups": ["yuk_markazi_gruppaaaa", "YUK_MARKAZI_XIZMATI"]},
    {"session": "acc2", "api_id": 27622829, "api_hash": "070517eac99d...", "source_groups": ["Yuk_markazi_yukmarkazi", "lorry_uzbek"]},
    {"session": "acc3", "api_id": 28796243, "api_hash": "59915e8540fe...", "source_groups": ["Surxondaryoyukmarkazi", "yukmarkazi_isuzuchilar"]},
]

MY_GROUP = "yukmarkazi_isuzular"
BLOCKED_SENDERS = {"Majbur_bot", "tg_botlar"}

account_semaphores = {}


async def retry_with_backoff(coro_func, *args, max_tries=5, base=1.5):
    tries = 0
    while tries < max_tries:
        try:
            return await coro_func(*args)
        except FloodWaitError as e:
            wait = e.seconds + 1
            print(f"[retry] FloodWaitError: kutilyapti {wait}s")
            await asyncio.sleep(wait)
        except RPCError as e:
            tries += 1
            wait = base ** tries + random.random()
            print(f"[retry] RPCError ({e}). kutilyapti {wait:.1f}s, urinish {tries}/{max_tries}")
            await asyncio.sleep(wait)
        except Exception as e:
            tries += 1
            wait = base ** tries + random.random()
            print(f"[retry] Other error ({e}). kutilyapti {wait:.1f}s, urinish {tries}/{max_tries}")
            await asyncio.sleep(wait)
    raise RuntimeError("Max retry attempts reached")


async def forward_message(client, my_group_entity, event, account_name):
    try:
        chat = await event.get_chat()
        chat_title = getattr(chat, "title", None) or getattr(chat, "username", None) or str(event.chat_id)
    except:
        chat_title = str(event.chat_id)

    try:
        sender = await event.get_sender()
        sender_name = sender.username if sender and getattr(sender, "username", None) else (
            getattr(sender, "first_name", "unknown") or str(getattr(sender, "id", "unknown"))
        )
    except:
        sender_name = "unknown"

    text = event.raw_text or ""
    clean_text = re.sub(r'@\w+', '', text).strip()

    print(f"[{account_name}] Manba: {chat_title} | Yuborgan: {sender_name} | Text len: {len(clean_text)}")

    sem = account_semaphores[account_name]
    async with sem:
        async def do_forward():
            if clean_text:
                await client.send_message(my_group_entity, clean_text)
                return "sent_clean_text"
            elif event.media:
                await event.forward_to(my_group_entity)
                return "forwarded_media"

        result = await retry_with_backoff(do_forward)
        print(f"[{account_name}] {result} ({chat_title} -> {MY_GROUP})")


async def run_client(account):
    name = account["session"]
    account_semaphores[name] = asyncio.Semaphore(1)
    client = TelegramClient(name, account["api_id"], account["api_hash"])

    await client.start()
    try:
        my_group_entity = await client.get_entity(MY_GROUP)
    except Exception as e:
        print(f"[{name}] MY_GROUP olinmadi: {e}; fallback to username")
        my_group_entity = MY_GROUP

    groups = account.get("source_groups", [])
    print(f"[{name}] ishga tushdi. Kuzatiladi: {groups}")

    @client.on(events.NewMessage(chats=groups))
    async def handler(event):
        try:
            sender = await event.get_sender()
            if sender and getattr(sender, "username", None) in BLOCKED_SENDERS:
                print(f"[{name}] BLOCKED sender {sender.username}")
                return
        except:
            pass

        asyncio.create_task(forward_message(client, my_group_entity, event, name))

    await client.run_until_disconnected()


async def main():
    tasks = [run_client(acc) for acc in accounts]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    print("▶️ Fast forwarder starting (DB yo‘q, to‘g‘ridan-to‘g‘ri forward)...")
    asyncio.run(main())
# faxriddin
