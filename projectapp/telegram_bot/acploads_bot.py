import asyncio
import random
import re
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError, RPCError, UsernameNotOccupiedError
from telethon.tl.types import ChannelForbidden  # <-- bu kerak
from telethon.sessions import StringSession

# ====== MOSLASHTIRING ======
accounts = [
    {"session": None, "api_id": 21825034, "api_hash": "54914cdafa40fbb22d574799c0f38a9e", "source_groups": ["yuk_markazi_gruppaaaa","Surxondaryoyukmarkazi"]}
]

MY_GROUP = "yukmarkazi_isuzular"

BLOCKED_SENDERS = {"Majbur_bot", "tg_botlar"}
BLOCKED_BOTS = {"Qorovuldodabot", "Tozalovchimrobot", "QorovulBot", "Tozalovchimbot"}

account_semaphores = {}

# ===== Retry helper =====
async def retry_with_backoff(coro_func, max_tries=5, base=1.5):
    tries = 0
    while tries < max_tries:
        try:
            return await coro_func()
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

# ===== Forward function =====
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

    sender_username = getattr(sender, "username", None) if sender else None
    sender_id = getattr(sender, "id", None) if sender else None
    sender_display = ((getattr(sender, "first_name", "") or "") + " " + (getattr(sender, "last_name", "") or "")).strip() or str(sender_id) if sender else "channel_or_unknown"

    text = event.raw_text or ""
    clean_text = re.sub(r'@\w+', '', text).strip()

    if getattr(event, "media", None):
        print(f"[{account_name}] ❌ Media xabar tashlanmadi ({chat_title})")
        return
    if sender_username and (sender_username in BLOCKED_BOTS or sender_username in BLOCKED_SENDERS):
        print(f"[{account_name}] ❌ Blocklangan username ({sender_username}) sabab tashlanmadi ({chat_title})")
        return
    if "virtual" in clean_text.lower():
        print(f"[{account_name}] ❌ 'virtual' so'zi sabab xabar tashlanmadi ({chat_title})")
        return
    if not clean_text:
        print(f"[{account_name}] ❌ Text bo'sh — tashlanmadi ({chat_title})")
        return

    owner_link = f"https://t.me/{sender_username}" if sender_username else f"tg://user?id={sender_id}" if sender_id else "Noma'lum"
    final_text = f"{clean_text}\n\nYuk egasi: {owner_link}"

    print(f"[{account_name}] Manba: {chat_title} | Yuborgan: {sender_display} ({sender_username or 'no-username'}) | Len: {len(clean_text)}")

    sem = account_semaphores[account_name]
    async with sem:
        async def do_forward():
            await client.send_message(my_group_entity, final_text)
            return "sent_clean_text_with_owner"

        result = await retry_with_backoff(do_forward)
        print(f"[{account_name}] {result} ({chat_title} -> {MY_GROUP})")

# ===== Client runner =====
async def run_client(account):
    name = f"temp_{random.randint(1000,9999)}"
    account_semaphores[name] = asyncio.Semaphore(1)

    client = TelegramClient(StringSession(), account["api_id"], account["api_hash"])
    await client.start()

    try:
        my_group_entity = await client.get_entity(MY_GROUP)
        print(f"[{name}] MY_GROUP resolved: {my_group_entity}")
    except Exception as e:
        print(f"[{name}] MY_GROUP olinmadi: {e}. Fallback: {MY_GROUP}")
        my_group_entity = MY_GROUP

    resolved = []
    for g in account.get("source_groups", []):
        try:
            ent = await client.get_entity(g)
            if isinstance(ent, ChannelForbidden):
                print(f"[{name}] ❌ {g} — ChannelForbidden. Skipped.")
                continue
            resolved.append(ent)
            print(f"[{name}] group '{g}' resolved -> {ent}")
        except UsernameNotOccupiedError:
            print(f"[{name}] group '{g}' — username mavjud emas. Skipped.")
        except Exception as e:
            print(f"[{name}] group '{g}' — boshqa xato ({e}). Skipped.")

    if not resolved:
        print(f"[{name}] Hech qanday source_group resolve bo'lmadi. Hech narsa kuzatilmaydi.")
    else:
        print(f"[{name}] Ishga tushdi. Kuzatiladigan resolved guruhlar: {resolved}")

        @client.on(events.NewMessage(chats=tuple(resolved)))
        async def handler(event):
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

# ===== Main =====
async def main():
    tasks = [run_client(acc) for acc in accounts]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    print("▶️ Fast forwarder starting (DB yo‘q, to‘g‘ridan-to‘g‘ri forward, sessiyasiz)...")
    asyncio.run(main())
