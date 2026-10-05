import re
from typing import List, Optional
import bot_config as config
from filter import normalize_phones_in_text


def clean_raw_text(text: str) -> str:
    """
    Xabardagi keraksiz bot buyruqlari, qora bot havolalari va ortiqcha belgilarni tozalash.
    """
    if not text:
        return ""

    # Bot havolalari yoki guruh reklamalari (@username) ni tozalash, lekin telefonlarni saqlash
    cleaned = re.sub(r'https?://t\.me/[\w_]+', '', text)
    cleaned = re.sub(r'@[a-zA-Z0-9_]+bot\b', '', cleaned, flags=re.IGNORECASE)

    # Foydalanuvchi iltimosiga ko'ra: barcha keraksiz hashtag (#) reshotkalarni olib tashlaymiz
    cleaned = re.sub(r'#\w+', '', cleaned)

    # Telefon raqamlarni Telegramda to'g'ridan-to'g'ri ko'k bo'lib bosiladigan formatga o'tkazish
    cleaned = normalize_phones_in_text(cleaned)

    # Ko'p qatorli bo'shliqlarni bitta bo'shliqqa keltirish
    lines = [line.strip() for line in cleaned.splitlines() if line.strip()]
    return "\n".join(lines)


def format_cargo_post(
    raw_text: str,
    phones: List[str],
    sender_username: Optional[str] = None,
    sender_id: Optional[int] = None,
    sender_first_name: Optional[str] = None,
    source_title: Optional[str] = None,
) -> str:
    """
    Yuk xabarini senior darajada, toza, ortiqcha belgilarsiz (reshotkalarsiz),
    va telefon raqamlar Telegramda ko'k bo'lib bosiladigan holatda shakllantiradi.
    """
    cleaned_text = clean_raw_text(raw_text)

    # 1. Aloqa raqamlarini chiqarish (Telegramda ko'k bo'lib chiqishi uchun +998... probelsiz format)
    phone_lines = []
    for p in phones:
        phone_lines.append(f"📞 <b>Telefon:</b> {p}")

    phones_formatted = "\n".join(phone_lines)

    # 2. Yuk egasining telegram profili (ortiqcha smaylik va xunuk belgilardan tozalangan)
    owner_line = ""
    if sender_username:
        owner_line = f"\n👤 <b>Telegram:</b> @{sender_username}"
    elif sender_id:
        # Xavfsiz havola - profil ismidagi portlovchi yoki g'alati belgilarni chiqarmaydi
        owner_line = f'\n👤 <b>Telegram:</b> <a href="tg://user?id={sender_id}">Yuk egasiga yozish</a>'

    # 3. Yakuniy estetik post shabloni (Reshotkalarsiz, toza va professional)
    post = (
        f"🚚 <b>YANGI YUK BUYURTMASI</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"{cleaned_text}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"{phones_formatted}"
        f"{owner_line}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👉 <b>Guruhimiz:</b> @{config.DESTINATION_GROUP}\n"
        f"🔗 <b>Havola:</b> https://t.me/{config.DESTINATION_GROUP}"
    )

    return post
