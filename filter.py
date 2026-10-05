import re
import time
import hashlib
from collections import OrderedDict
from typing import List, Optional
import bot_config as config

# O'zbekiston mobil operator kodlari
UZ_OPERATOR_PREFIXES = r'(?:90|91|93|94|95|97|98|99|88|33|77|50|20)'

# 1. To'liq O'zbekiston formati: (+998 yoki 998 bilan)
REGEX_UZ_FULL = re.compile(
    r'(?:\+?998)[\s\-\.]*\(?' + UZ_OPERATOR_PREFIXES + r'\)?[\s\-\.]*\d{3}[\s\-\.]*\d{2}[\s\-\.]*\d{2}',
    re.IGNORECASE
)

# 2. Qisqa O'zbekiston formati: (90 123 45 67, (90) 123-45-67, 90.123.45.67)
REGEX_UZ_SHORT = re.compile(
    r'(?:^|[\s:;,/(])\(?(' + UZ_OPERATOR_PREFIXES + r')\)?[\s\-\.]*(\d{3})[\s\-\.]*(\d{2})[\s\-\.]*(\d{2})(?:$|[^\d])',
    re.IGNORECASE
)

# 3. Xalqaro format (Rossiya, Qozog'iston, Qirg'iziston, Tojikiston)
REGEX_INTL = re.compile(
    r'(?:\+7|8)[\s\-\.]*\(?\d{3}\)?[\s\-\.]*\d{3}[\s\-\.]*\d{2}[\s\-\.]*\d{2}|'
    r'\+996[\s\-\.]*\d{3}[\s\-\.]*\d{3}[\s\-\.]*\d{3}|'
    r'\+992[\s\-\.]*\d{2}[\s\-\.]*\d{3}[\s\-\.]*\d{4}',
    re.IGNORECASE
)


def extract_phone_numbers(text: str) -> List[str]:
    """
    Matndan barcha haqiqiy telefon raqamlarini ajratib oladi va 
    Telegramda KO'K (bosganda darhol tel qiladigan) formatga keltiradi:
    Masalan: ['+998904060987', '+998994093134']
    """
    if not text:
        return []

    found = []
    seen_digits = set()

    # 1. To'liq O'zbekiston raqamlari
    for match in REGEX_UZ_FULL.finditer(text):
        raw = match.group(0)
        digits = re.sub(r'\D', '', raw)
        if digits.startswith('998') and len(digits) == 12:
            if digits not in seen_digits:
                seen_digits.add(digits)
                found.append(f"+{digits}")

    # 2. Qisqa O'zbekiston raqamlari (99 409 31 34)
    for match in REGEX_UZ_SHORT.finditer(text):
        code = match.group(1)
        part1 = match.group(2)
        part2 = match.group(3)
        part3 = match.group(4)
        digits = f"998{code}{part1}{part2}{part3}"
        if digits not in seen_digits and len(digits) == 12:
            seen_digits.add(digits)
            found.append(f"+{digits}")

    # 3. Xalqaro raqamlar (+7, +996, +992)
    for match in REGEX_INTL.finditer(text):
        raw = match.group(0).strip()
        digits = re.sub(r'\D', '', raw)
        if digits and digits not in seen_digits:
            seen_digits.add(digits)
            if digits.startswith("8") and len(digits) == 11:
                phone = f"+7{digits[1:]}"
            elif raw.startswith("+"):
                phone = f"+{digits}"
            else:
                phone = f"+{digits}"
            found.append(phone)

    return found


def normalize_phones_in_text(text: str) -> str:
    """
    Xabar matni ichidagi orasi ochiq yozilgan raqamlarni (masalan: 99 409 31 34 yoki +998 (91) 118-22-04)
    Telegramda to'g'ridan-to'g'ri ko'k bo'lib bosiladigan '+998994093134' formatga o'zgartiradi.
    """
    if not text:
        return ""

    # 1. To'liq formatni almashtirish (+998 90 123 45 67 -> +998901234567)
    def repl_full(m):
        digits = re.sub(r'\D', '', m.group(0))
        return f" +{digits} "

    text = REGEX_UZ_FULL.sub(repl_full, text)

    # 2. Qisqa formatni almashtirish (99 409 31 34 -> +998994093134)
    def repl_short(m):
        prefix = m.group(1) if m.group(1) else ""
        code = m.group(2)
        p1 = m.group(3)
        p2 = m.group(4)
        p3 = m.group(5)
        suffix = m.group(6) if m.group(6) else ""
        return f"{prefix}+{998}{code}{p1}{p2}{p3}{suffix}"

    short_pattern = re.compile(
        r'(^|[\s:;,/(])\(?(' + UZ_OPERATOR_PREFIXES + r')\)?[\s\-\.]*(\d{3})[\s\-\.]*(\d{2})[\s\-\.]*(\d{2})($|[^\d])',
        re.IGNORECASE
    )
    text = short_pattern.sub(repl_short, text)

    return text


def is_spam_or_bot(text: str, sender_username: Optional[str] = None, is_bot: bool = False) -> bool:
    """
    Keraksiz botlar, to'lov xabarlari, reklama va spamni aniqlash.
    """
    if is_bot:
        return True

    if sender_username:
        u_lower = sender_username.lower()
        if u_lower.endswith("bot") or u_lower in config.BLOCKED_BOTS:
            return True

    if not text:
        return True

    text_lower = text.lower()

    for kw in config.SPAM_KEYWORDS:
        if kw in text_lower:
            return True

    return False


class InMemoryDedupCache:
    """
    100% RAM dagi xotira (Server diskini to'ldirmaydi).
    Bir xil yuk takroran tushishini oldini oladi.
    """
    def __init__(self, max_size: int = config.MAX_CACHE_SIZE, ttl_seconds: int = config.DEDUP_TTL_SECONDS):
        self.max_size = max_size
        self.ttl = ttl_seconds
        self.cache: OrderedDict[str, float] = OrderedDict()

    def _generate_key(self, phones: List[str], text: str) -> str:
        phone_part = "_".join(sorted(phones)) if phones else ""
        words = re.findall(r'\w+', text.lower())[:15]
        text_signature = " ".join(words)
        raw_key = f"{phone_part}::{text_signature}"
        return hashlib.md5(raw_key.encode("utf-8")).hexdigest()

    def is_duplicate(self, phones: List[str], text: str) -> bool:
        now = time.time()
        key = self._generate_key(phones, text)

        if key in self.cache:
            created_at = self.cache[key]
            if now - created_at < self.ttl:
                self.cache.move_to_end(key)
                return True
            else:
                del self.cache[key]

        if len(self.cache) >= self.max_size:
            self.cache.popitem(last=False)

        self.cache[key] = now
        return False


dedup_cache = InMemoryDedupCache()
