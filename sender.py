import asyncio
import aiohttp
import logging
from typing import Optional
from telethon import TelegramClient
from telethon.errors import FloodWaitError, RPCError
import bot_config as config

logger = logging.getLogger("Sender")

# Telegram Bot API xabarlar yuborish uchun sessiya
_session: Optional[aiohttp.ClientSession] = None
_send_semaphore = asyncio.Semaphore(5)  # Bir vaqtning o'zida parallel xavfsiz yuborish


async def get_http_session() -> aiohttp.ClientSession:
    global _session
    if _session is None or _session.closed:
        _session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=10)
        )
    return _session


async def send_via_bot(text: str, chat_id: str = f"@{config.DESTINATION_GROUP}") -> bool:
    """
    Telegram Bot API orqali yuqori tezlikda (mikrosoniyalarda) guruhga xabar yuborish.
    Bu foydalanuvchi akkauntini cheklovlarga tushishdan asraydi.
    """
    url = f"https://api.telegram.org/bot{config.BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }

    session = await get_http_session()

    for attempt in range(3):
        try:
            async with _send_semaphore:
                async with session.post(url, json=payload) as resp:
                    data = await resp.json()
                    if resp.status == 200 and data.get("ok"):
                        return True

                    if resp.status == 429:
                        retry_after = data.get("parameters", {}).get("retry_after", 3)
                        print(f"⚠️ [Bot API] Rate limit (Flood): {retry_after} soniya kutilmoqda...")
                        await asyncio.sleep(retry_after)
                        continue

                    print(f"❌ [Bot API Xatosi]: {data.get('description')}")
                    return False
        except Exception as e:
            await asyncio.sleep(1)

    return False


async def send_via_userbot(client: TelegramClient, text: str, dest_entity) -> bool:
    """
    Agar bot token ishlamasa yoki bot guruhda admin bo'lmasa,
    to'g'ridan-to'g'ri userbot orqali guruhga yuborish (Fallback).
    """
    for attempt in range(3):
        try:
            async with _send_semaphore:
                await client.send_message(
                    dest_entity,
                    text,
                    parse_mode="html",
                    link_preview=False
                )
                return True
        except FloodWaitError as e:
            print(f"⚠️ [Userbot Flood]: {e.seconds} soniya kutish...")
            await asyncio.sleep(e.seconds + 1)
        except RPCError as e:
            print(f"❌ [Userbot RPC xatosi]: {e}")
            await asyncio.sleep(2)
        except Exception as e:
            print(f"❌ [Userbot xatosi]: {e}")
            await asyncio.sleep(1)

    return False


async def dispatch_cargo_message(text: str, userbot_client: Optional[TelegramClient] = None, dest_entity = None) -> bool:
    """
    Guruhga xabar yuborish dispetcheri:
    Oldin bot orqali yuborishga harakat qiladi, agar o'xshamasa userbot orqali yuboradi.
    """
    # 1. Bot orqali yuborish
    if config.SEND_MODE == "bot" and config.BOT_TOKEN:
        success = await send_via_bot(text)
        if success:
            return True

    # 2. Agar bot bilan bo'lmasa yoki SEND_MODE userbot bo'lsa
    if userbot_client and dest_entity:
        return await send_via_userbot(userbot_client, text, dest_entity)

    return False
