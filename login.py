import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import bot_config as config

print("=" * 60)
print("🔑 YUK MARKAZI TELEGRAM USERBOT KIRISH (LOGIN) TIZIMI")
print("=" * 60)
print(f"📌 API ID: {config.API_ID}")
print(f"📌 API HASH: {config.API_HASH[:8]}...")
print("=" * 60)
print("Iltimos, telefon raqamingizni xalqaro formatda kiriting (masalan: +998901234567)")

try:
    with TelegramClient(StringSession(), config.API_ID, config.API_HASH) as client:
        session_str = client.session.save()
        
        # 1. session.txt fayliga saqlash
        with open(config.SESSION_FILE, "w", encoding="utf-8") as f:
            f.write(session_str)

        # 2. .env fayliga ham avtomatik saqlab qo'yish
        env_lines = []
        if os.path.exists(".env"):
            with open(".env", "r", encoding="utf-8") as f:
                env_lines = f.readlines()

        has_session = False
        new_env_lines = []
        for line in env_lines:
            if line.startswith("TG_SESSION_STRING="):
                new_env_lines.append(f"TG_SESSION_STRING={session_str}\n")
                has_session = True
            else:
                new_env_lines.append(line)

        if not has_session:
            new_env_lines.append(f"\nTG_SESSION_STRING={session_str}\n")

        with open(".env", "w", encoding="utf-8") as f:
            f.writelines(new_env_lines)

        me = client.get_me()
        print("\n" + "=" * 60)
        print("✅ TABRIKLAYMIZ! MUVAFAQIYATLI LOGIN QILINDI!")
        print(f"👤 Ism: {me.first_name} {me.last_name or ''}")
        print(f"🆔 Username: @{me.username or 'yoq'}")
        print(f"💾 Sessiya saqlandi: {config.SESSION_FILE}")
        print("Endi botni ishga tushirishingiz mumkin: python main.py")
        print("=" * 60)

except Exception as e:
    print(f"\n❌ Login jarayonida xatolik yuz berdi: {e}")
    sys.exit(1)
