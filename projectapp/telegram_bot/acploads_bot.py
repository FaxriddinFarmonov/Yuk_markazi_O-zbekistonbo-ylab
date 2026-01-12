import asyncio
import random
import re
import os

from telethon import TelegramClient, events
from telethon.errors import FloodWaitError, RPCError, UsernameNotOccupiedError
from telethon.sessions import StringSession
from telethon.tl.types import ChannelForbidden

# ====== MOSLASHTIRING ======
accounts = [
    {
        "api_id": 13289212,
        "api_hash": "a43b3238c55399fb49e5a529eb026342",
        "source_groups": ["yuk_markazi_gruppaaaa", "Surxondaryoyukmarkazi"],
        "session_file": "tg_session.txt",  # 👈 MUHIM
    }
]

MY_GROUP = "yukmarkazi_isuzular"

BLOCKED_SENDERS = {"Majbur_bot", "tg_botlar"}
BLOCKED_BOTS = {"Qorovuldodabot", "Tozalovchimrobot", "QorovulBot", "Tozalovchimbot"}

account_semaphores = {}

# ===== Session loader =====
def load_or_create_session(session_file: str):
    if os.path.exists(session_file):
        with open(session_file, "r") as f:
            session_str = f.read().strip()
            print("✅ Session fayldan yuklandi")
            return StringSession(session_str)
    else:
        print("🆕 Session yo‘q — yangi login qilinadi")
        return StringSession()

# ===== Retry helper =====
async def retry_with_backoff(coro_func, max_tries=5, base=1.5):
    tries = 0
    while tries < max_tries:
        try:
            return await coro_func()
        except FloodWaitError as e:
            wait = e.seconds + 1
            print(f"[retry] FloodWaitError: {wait}s kutilmoqda")
            await asyncio.sleep(wait)
        except RPCError as e:
            tries += 1
            wait = base ** tries + random.random()
            await asyncio.sleep(wait)
        except Exception as e:
            tries += 1
            wait = base ** tries + random.random()
            await asyncio.sleep(wait)
    raise RuntimeError("Max retry attempts reached")

# ===== Forward function =====
async def forward_message(client, my_group_entity, event, account_name):
    if event.media:
        return

    text = event.raw_text or ""
    clean_text = re.sub(r'@\w+', '', text).strip()

    if not clean_text or "virtual" in clean_text.lower():
        return

    sender = await event.get_sender()
    sender_username = getattr(sender, "username", None)
    sender_id = getattr(sender, "id", None)

    if sender_username and (sender_username in BLOCKED_SENDERS or sender_username in BLOCKED_BOTS):
        return

    owner_link = (
        f"https://t.me/{sender_username}"
        if sender_username
        else f"tg://user?id={sender_id}"
        if sender_id
        else "Noma'lum"
    )

    final_text = f"{clean_text}\n\nYuk egasi: {owner_link}"

    sem = account_semaphores[account_name]
    async with sem:
        async def do_send():
            await client.send_message(my_group_entity, final_text)

        await retry_with_backoff(do_send)

# ===== Client runner =====
async def run_client(account):
    name = "main_account"
    account_semaphores[name] = asyncio.Semaphore(1)

    session = load_or_create_session(account["session_file"])
    client = TelegramClient(session, account["api_id"], account["api_hash"])

    await client.start()

    # 🔥 Sessionni SAQLAB QO‘YAMIZ (faqat 1 marta login bo‘ladi)
    if not os.path.exists(account["session_file"]):
        with open(account["session_file"], "w") as f:
            f.write(client.session.save())
        print("💾 Session faylga saqlandi")

    my_group_entity = await client.get_entity(MY_GROUP)

    resolved = []
    for g in account["source_groups"]:
        try:
            ent = await client.get_entity(g)
            if isinstance(ent, ChannelForbidden):
                continue
            resolved.append(ent)
        except Exception:
            pass

    @client.on(events.NewMessage(chats=tuple(resolved)))
    async def handler(event):
        asyncio.create_task(forward_message(client, my_group_entity, event, name))

    await client.run_until_disconnected()

# ===== Main =====
async def main():
    await asyncio.gather(*(run_client(acc) for acc in accounts))

if __name__ == "__main__":
    print("▶️ Fast forwarder starting (1 marta login, session saqlanadi)...")
    asyncio.run(main())
