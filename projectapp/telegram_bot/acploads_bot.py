
#
# import asyncio
# import random
# import re
# from telethon import TelegramClient, events
# from telethon.errors import FloodWaitError, RPCError
#
# accounts = [
#     {"session": "acc1", "api_id": 21825034, "api_hash": "54914cdafa40f...", "source_groups": ["yuk_markazi_gruppaaaa", "YUK_MARKAZI_XIZMATI"]},
#     {"session": "acc2", "api_id": 27622829, "api_hash": "070517eac99d...", "source_groups": ["Yuk_markazi_yukmarkazi", "Surxondaryoyukmarkazi"]},
#     {"session": "acc3", "api_id": 28796243, "api_hash": "59915e8540fe...", "source_groups": ["lorry_uzbek", "yukmarkazi_isuzuchilar"]},
# ]
#
# MY_GROUP = "yukmarkazi_isuzular"
# BLOCKED_SENDERS = {"Majbur_bot", "tg_botlar"}
#
# account_semaphores = {}
#
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
#
# async def forward_message(client, my_group_entity, event, account_name):
#     try:
#         chat = await event.get_chat()
#         chat_title = getattr(chat, "title", None) or getattr(chat, "username", None) or str(event.chat_id)
#     except:
#         chat_title = str(event.chat_id)
#
#     try:
#         sender = await event.get_sender()
#         sender_name = sender.username if sender and getattr(sender, "username", None) else (
#             getattr(sender, "first_name", "unknown") or str(getattr(sender, "id", "unknown"))
#         )
#     except:
#         sender_name = "unknown"
#
#     text = event.raw_text or ""
#     clean_text = re.sub(r'@\w+', '', text).strip()
#
#     print(f"[{account_name}] Manba: {chat_title} | Yuborgan: {sender_name} | Text len: {len(clean_text)}")
#
#     sem = account_semaphores[account_name]
#     async with sem:
#         async def do_forward():
#             if clean_text:
#                 await client.send_message(my_group_entity, clean_text)
#                 return "sent_clean_text"
#             elif event.media:
#                 await event.forward_to(my_group_entity)
#                 return "forwarded_media"
#
#         result = await retry_with_backoff(do_forward)
#         print(f"[{account_name}] {result} ({chat_title} -> {MY_GROUP})")
#
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
#         try:
#             sender = await event.get_sender()
#             if sender and getattr(sender, "username", None) in BLOCKED_SENDERS:
#                 print(f"[{name}] BLOCKED sender {sender.username}")
#                 return
#         except:
#             pass
#
#         asyncio.create_task(forward_message(client, my_group_entity, event, name))
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
#     print("▶️ Fast forwarder starting (DB yo‘q, to‘g‘ridan-to‘g‘ri forward)...")
#     asyncio.run(main())
# # faxriddin

#
#
# import asyncio
# import random
# import re
# from telethon import TelegramClient, events
# from telethon.errors import FloodWaitError, RPCError
#
# accounts = [
#     {"session": "acc1", "api_id": 21825034, "api_hash": "54914cdafa40f...", "source_groups": ["yuk_markazi_gruppaaaa", "YUK_MARKAZI_XIZMATI"]},
#     {"session": "acc2", "api_id": 27622829, "api_hash": "070517eac99d...", "source_groups": ["Yuk_markazi_yukmarkazi", "Surxondaryoyukmarkazi"]},
#     {"session": "acc3", "api_id": 28796243, "api_hash": "59915e8540fe...", "source_groups": ["lorry_uzbek", "yukmarkazi_isuzuchilar"]},
# ]
#
# MY_GROUP = "yukmarkazi_isuzular"
#
# # ❌ Block qilinadigan foydalanuvchilar
# BLOCKED_SENDERS = {"Majbur_bot", "tg_botlar"}
# BLOCKED_BOTS = {"Qorovuldodabot", "Tozalovchimrobot", "QorovulBot", "Tozalovchimbot"}
#
# account_semaphores = {}
#
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
#
# async def forward_message(client, my_group_entity, event, account_name):
#     try:
#         chat = await event.get_chat()
#         chat_title = getattr(chat, "title", None) or getattr(chat, "username", None) or str(event.chat_id)
#     except:
#         chat_title = str(event.chat_id)
#
#     try:
#         sender = await event.get_sender()
#         sender_name = sender.username if sender and getattr(sender, "username", None) else (
#             getattr(sender, "first_name", "unknown") or str(getattr(sender, "id", "unknown"))
#         )
#     except:
#         sender_name = "unknown"
#
#     text = event.raw_text or ""
#     clean_text = re.sub(r'@\w+', '', text).strip()
#
#     # ❌ Filtrlash: Media xabarlar o‘tkazilmaydi
#     if event.media:
#         print(f"[{account_name}] ❌ Media xabar tashlanmadi ({chat_title})")
#         return
#
#     # ❌ Filtrlash: Block qilingan botlardan kelgan xabarlar
#     if sender and getattr(sender, "username", None) in BLOCKED_BOTS:
#         print(f"[{account_name}] ❌ Blocklangan botdan xabar ({sender.username}) tashlanmadi")
#         return
#
#     # ❌ Filtrlash: Matnda "virtual" so‘zi bor bo‘lsa
#     if "virtual" in clean_text.lower():
#         print(f"[{account_name}] ❌ Virtual so‘zi borligi sabab tashlanmadi ({chat_title})")
#         return
#
#     print(f"[{account_name}] Manba: {chat_title} | Yuborgan: {sender_name} | Text len: {len(clean_text)}")
#
#     sem = account_semaphores[account_name]
#     async with sem:
#         async def do_forward():
#             if clean_text:
#                 await client.send_message(my_group_entity, clean_text)
#                 return "sent_clean_text"
#
#         result = await retry_with_backoff(do_forward)
#         print(f"[{account_name}] {result} ({chat_title} -> {MY_GROUP})")
#
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
#         try:
#             sender = await event.get_sender()
#             if sender and getattr(sender, "username", None) in BLOCKED_SENDERS:
#                 print(f"[{name}] BLOCKED sender {sender.username}")
#                 return
#         except:
#             pass
#
#         asyncio.create_task(forward_message(client, my_group_entity, event, name))
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
#     print("▶️ Fast forwarder starting (DB yo‘q, to‘g‘ridan-to‘g‘ri forward)...")
#     asyncio.run(main())




import asyncio
import random
import re
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError, RPCError, UsernameNotOccupiedError

# ====== MOSLASHTIRING ======
accounts = [
    {"session": "acc1", "api_id": 21825034, "api_hash": "54914cdafa40f...", "source_groups": ["yuk_markazi_gruppaaaa", "YUK_MARKAZI_XIZMATI"]},
    {"session": "acc2", "api_id": 27622829, "api_hash": "070517eac99d...", "source_groups": ["Yuk_markazi_yukmarkazi", "Surxondaryoyukmarkazi"]},
    {"session": "acc3", "api_id": 28796243, "api_hash": "59915e8540fe...", "source_groups": ["lorry_uzbek", "yukmarkazi_isuzuchilar"]},
]

# Target guruh (public username yoki -100... chat_id)
MY_GROUP = "yukmarkazi_isuzular"
# ===========================

BLOCKED_SENDERS = {"Majbur_bot", "tg_botlar"}
BLOCKED_BOTS = {"Qorovuldodabot", "Tozalovchimrobot", "QorovulBot", "Tozalovchimbot"}

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
    except Exception:
        chat_title = str(event.chat_id)

    try:
        sender = await event.get_sender()
    except Exception:
        sender = None

    if sender:
        sender_username = getattr(sender, "username", None)
        sender_id = getattr(sender, "id", None)
        sender_display = (getattr(sender, "first_name", "") or "") + " " + (getattr(sender, "last_name", "") or "")
        sender_display = sender_display.strip() or str(sender_id)
    else:
        sender_username = None
        sender_id = None
        sender_display = "channel_or_unknown"

    text = event.raw_text or ""
    clean_text = re.sub(r'@\w+', '', text).strip()

    # 1) Media => tashlamaydi
    if getattr(event, "media", None):
        print(f"[{account_name}] ❌ Media xabar tashlanmadi ({chat_title})")
        return

    # 2) Block qilingan botlar yoki senders
    if sender_username and (sender_username in BLOCKED_BOTS or sender_username in BLOCKED_SENDERS):
        print(f"[{account_name}] ❌ Blocklangan username ({sender_username}) sabab tashlanmadi ({chat_title})")
        return

    # 3) "virtual" so'zi
    if "virtual" in clean_text.lower():
        print(f"[{account_name}] ❌ 'virtual' so'zi sabab xabar tashlanmadi ({chat_title})")
        return

    # 4) Bo'sh text => tashlamaydi
    if not clean_text:
        print(f"[{account_name}] ❌ Text bo'sh — tashlanmadi ({chat_title})")
        return

    # Yuk egasi link
    if sender_username:
        owner_link = f"https://t.me/{sender_username}"
    elif sender_id:
        owner_link = f"tg://user?id={sender_id}"
    else:
        owner_link = "Noma'lum"

    final_text = f"{clean_text}\n\nYuk egasi: {owner_link}"

    print(f"[{account_name}] Manba: {chat_title} | Yuborgan: {sender_display} ({sender_username or 'no-username'}) | Len: {len(clean_text)}")

    sem = account_semaphores[account_name]
    async with sem:
        async def do_forward():
            await client.send_message(my_group_entity, final_text)
            return "sent_clean_text_with_owner"

        result = await retry_with_backoff(do_forward)
        print(f"[{account_name}] {result} ({chat_title} -> {MY_GROUP})")


async def run_client(account):
    name = account["session"]
    account_semaphores[name] = asyncio.Semaphore(1)
    client = TelegramClient(name, account["api_id"], account["api_hash"])

    await client.start()
    # --- MY_GROUP resolve qilish (safe)
    try:
        my_group_entity = await client.get_entity(MY_GROUP)
        print(f"[{name}] MY_GROUP resolved: {my_group_entity}")
    except Exception as e:
        print(f"[{name}] MY_GROUP olinmadi: {e}. Fallback: {MY_GROUP}")
        my_group_entity = MY_GROUP

    # --- source_groups resolve qilish (username yoki ID yoki title bo'lishi mumkin)
    raw_groups = account.get("source_groups", [])
    resolved = []
    for g in raw_groups:
        # Agar foydalanuvchi oldindan -100... tarzida ID bergan bo'lsa
        try:
            if isinstance(g, str) and (g.startswith("-100") or g.isdigit()):
                gid = int(g)
                resolved.append(gid)
                print(f"[{name}] group '{g}' interpreted as id {gid}")
                continue
        except Exception:
            pass

        # Boshqa holatda - client.get_entity yordamida resolve qilib ko'ramiz
        try:
            ent = await client.get_entity(g)
            resolved.append(ent)
            print(f"[{name}] group '{g}' resolved -> {ent}")
        except UsernameNotOccupiedError:
            print(f"[{name}] group '{g}' — username mavjud emas (UsernameNotOccupied). Skipped.")
        except ValueError as ve:
            # Telethon ba'zan ValueError: No user has "..." as username
            print(f"[{name}] group '{g}' — ValueError ({ve}). Skipped.")
        except Exception as e:
            print(f"[{name}] group '{g}' — boshqa xato ({e}). Skipped.")

    if not resolved:
        print(f"[{name}] Hech qanday source_group resolve bo'lmadi. Hech narsa kuzatilmaydi.")
    else:
        print(f"[{name}] Ishga tushdi. Kuzatiladigan resolved guruhlar: {resolved}")

        # Hanuz handlerni resolved list bilan qo'yamiz
        @client.on(events.NewMessage(chats=tuple(resolved)))
        async def handler(event):
            # Pre-check: skip blocked senders asap
            try:
                sender = await event.get_sender()
                s_un = getattr(sender, "username", None)
                if s_un and (s_un in BLOCKED_SENDERS or s_un in BLOCKED_BOTS):
                    print(f"[{name}] BLOCKED sender pre-check: {s_un}")
                    return
            except Exception:
                pass

            asyncio.create_task(forward_message(client, my_group_entity, event, name))

    await client.run_until_disconnected()


async def main():
    tasks = [run_client(acc) for acc in accounts]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    print("▶️ Fast forwarder starting (DB yo‘q, to‘g‘ridan-to‘g‘ri forward)...")
    asyncio.run(main())
