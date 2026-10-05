import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import asyncio
import datetime
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import ChannelForbidden

import bot_config as config
from filter import extract_phone_numbers, is_spam_or_bot, dedup_cache
from formatter import format_cargo_post
from sender import dispatch_cargo_message


def load_session() -> StringSession:
    """
    Sessiyani .env dan yoki session.txt faylidan xotiraga yuklash.
    """
    session_str = os.getenv("TG_SESSION_STRING")
    if not session_str and os.path.exists(config.SESSION_FILE):
        try:
            with open(config.SESSION_FILE, "r", encoding="utf-8") as f:
                session_str = f.read().strip()
        except Exception:
            session_str = None

    if not session_str:
        print("\n" + "!" * 65)
        print("❌ XATOLIK: Telegram hisob sessiyasi topilmadi!")
        print("Iltimos, avval bitta buyruq orqali hisobingizga kiring:")
        print("   👉 python login.py")
        print("Telegramdan kelgan kodni kiritsangiz, sessiya avtomatik saqlanadi.")
        print("!" * 65 + "\n")
        sys.exit(1)

    return StringSession(session_str)


def load_source_groups() -> list:
    """
    groups.txt faylidan yoki configdan guruhlar ro'yxatini yuklash.
    """
    groups = []

    if os.path.exists("groups.txt"):
        try:
            with open("groups.txt", "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    # Havolalarni tozalash (https://t.me/guruh -> guruh)
                    clean_group = line.replace("https://t.me/", "").replace("http://t.me/", "").replace("t.me/", "").replace("@", "").strip()
                    if clean_group and clean_group not in groups:
                        groups.append(clean_group)
        except Exception as e:
            print(f"⚠️ groups.txt o'qishda ogohlantirish: {e}")

    if not groups:
        groups = list(config.DEFAULT_SOURCE_GROUPS)

    return groups


async def process_incoming_message(client: TelegramClient, dest_entity, event):
    """
    Har bir kelgan xabarni millisekundlarda qayta ishlash.
    Eslatma: Xabar manba guruhda darhol o'chirib yuborilsa ham,
    bizning bot uni MTProto orqali allaqachon xotiraga olib bo'lgan bo'ladi!
    """
    try:
        # 1. Matn mavjudligini tekshirish
        raw_text = event.raw_text or ""
        if len(raw_text.strip()) < 8:
            return

        # 2. Yuboruvchini aniqlash
        sender = await event.get_sender()
        sender_username = getattr(sender, "username", None)
        sender_id = getattr(sender, "id", None)
        sender_name = getattr(sender, "first_name", None)
        is_bot = getattr(sender, "bot", False)

        # 3. Spam, reklama yoki bot xabarlarini tekshirish
        if is_spam_or_bot(raw_text, sender_username, is_bot):
            return

        # 4. MUHIM: Faqat haqiqiy telefon raqami bor yuk xabarlarini ajratib olish!
        phones = extract_phone_numbers(raw_text)
        if not phones:
            # Telefon raqami bo'lmagan keraksiz gaplar yoki savollarni o'tkazib yuboramiz
            return

        # 5. Kesh orqali dublikatlarni tekshirish (100% RAM, disk to'lmaydi)
        if dedup_cache.is_duplicate(phones, raw_text):
            return

        # 6. Postni chiroyli va senior darajasida shakllantirish
        chat = await event.get_chat()
        chat_title = getattr(chat, "title", "Guruh")

        formatted_message = format_cargo_post(
            raw_text=raw_text,
            phones=phones,
            sender_username=sender_username,
            sender_id=sender_id,
            sender_first_name=sender_name,
            source_title=chat_title,
        )

        # 7. Guruhga yuborish (Bot API yoki Userbot orqali)
        success = await dispatch_cargo_message(
            text=formatted_message,
            userbot_client=client,
            dest_entity=dest_entity,
        )

        if success:
            now_str = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"[{now_str}] 🚀 YUK YUBORILDI: {phones[0][0]} | Manba: {chat_title}")

    except Exception as e:
        now_str = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"[{now_str}] ⚠️ Qayta ishlash xatosi: {e}")


async def main():
    print("=" * 65)
    print("⚡️ YUK MARKAZI FAST FORWARDER ENGINE (SENIOR EDITION)")
    print("=" * 65)
    print("🚀 Tizim ishga tushmoqda...")
    print(f"📦 Maqsad guruh: @{config.DESTINATION_GROUP}")
    print(f"🛡 Xotira rejimi: 100% In-Memory RAM (Diskka log va baza yozilmaydi)")
    print(f"⚡️ Tezlik: Real-Time MTProto Stream (O'chirilgan xabarlarni ham ilib oladi)")

    session = load_session()
    client = TelegramClient(session, config.API_ID, config.API_HASH)

    await client.start()
    me = await client.get_me()
    print(f"✅ Userbot hisobi ulandi: {me.first_name} (@{me.username or 'nom_yoq'})")

    # Maqsad guruh entity-sini olish
    try:
        dest_entity = await client.get_entity(config.DESTINATION_GROUP)
        print(f"✅ Maqsad guruh tasdiqlandi: @{config.DESTINATION_GROUP}")
    except Exception as e:
        print(f"⚠️ Maqsad guruhga ulanishda ogohlantirish: {e}")
        dest_entity = config.DESTINATION_GROUP

    # Manba guruhlarni aniqlash va tekshirish
    source_groups = load_source_groups()
    print(f"🔍 {len(source_groups)} ta manba guruhlar tahlil qilinmoqda...")

    resolved_entities = []
    for g in source_groups:
        try:
            ent = await client.get_entity(g)
            if isinstance(ent, ChannelForbidden):
                continue
            resolved_entities.append(ent)
            print(f"   🟢 Guruhga ulandi: {getattr(ent, 'title', g)}")
        except Exception:
            # Agar guruhga a'zo bo'linmagan bo'lsa yoki noto'g'ri bo'lsa
            pass

    if not resolved_entities:
        print("⚠️ Hozircha manba guruhlarga ulanib bo'lmadi.")
        print("Iltimos, 'groups.txt' fayliga o'zingiz a'zo bo'lgan yuk guruhlarini kiriting.")
        # Butun hisobdagi chatlar uchun tinglash imkoniyati
        listen_chats = None
    else:
        listen_chats = tuple(resolved_entities)
        print(f"🎯 Jami {len(resolved_entities)} ta yuk guruhi jonli rejimda tinglanmoqda...")

    # Real-time NewMessage hodisasi
    @client.on(events.NewMessage(chats=listen_chats))
    async def incoming_handler(event):
        # Asinxron navbatga tashlash - zarracha kechikish bo'lmaydi!
        asyncio.create_task(process_incoming_message(client, dest_entity, event))

    print("\n✅ TIZIM 100% TAYYOR! Jonli yuk xabarlari kutilmoqda...\n" + "-" * 65)
    await client.run_until_disconnected()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("\n🛑 Dastur to'xtatildi.")
