# dasdsadasdsa
import os
from dotenv import load_dotenv

# .env faylini yuklash
load_dotenv()

# Telegram API sozlamalari (my.telegram.org)
API_ID = int(os.getenv("TG_API_ID", "38151215"))
API_HASH = os.getenv("TG_API_HASH", "2e85c486c430a8cddd0f548c23cefdb3")

# Bot Father dan olingan bot token (@acploads_bot)
BOT_TOKEN = os.getenv("TG_BOT_TOKEN", "8653950102:AAGAksFentev_wGZZ67OmvxHa9ChFWYqmnw")

# Sizning qabul qiluvchi asosiy guruhingiz (username yoki ID)
DESTINATION_GROUP = os.getenv("TG_DESTINATION_GROUP", "Yuklar_markazitoplami")

# Userbot session saqlanadigan fayl (StringSession - serverda joy egallamaydi)
SESSION_FILE = os.getenv("TG_SESSION_FILE", "session.txt")

# Xabarlar yuborish rejimi: 'bot' (tavsiya etiladi) yoki 'userbot'
SEND_MODE = os.getenv("SEND_MODE", "bot")

# Server xotirasini tejash: deduplikatsiya uchun RAM dagi maksimal xabarlar soni
# Diskka HECH QANDAY baza yoki og'ir log yozilmaydi!
MAX_CACHE_SIZE = int(os.getenv("MAX_CACHE_SIZE", "5000"))

# Xabar takrorlanmasligi uchun eslab qolish vaqti (soniyalarda, masalan 3600 = 1 soat)
DEDUP_TTL_SECONDS = int(os.getenv("DEDUP_TTL_SECONDS", "3600"))

# Boshlang'ich yuk olinadigan guruhlar (Userbot a'zo bo'lgan har qanday ochiq/yopiq guruhlar)
DEFAULT_SOURCE_GROUPS = [
    "yuk_markazi_gruppaaaa",
    "Surxondaryoyukmarkazi",
    "yukmarkazi_isuzular",
]

# Qora ro'yxatdagi botlar va tizim username-lari
BLOCKED_BOTS = {
    "majbur_bot", "tg_botlar", "qorovuldodabot", "tozalovchimrobot",
    "qorovulbot", "tozalovchimbot", "cleanerbot", "shieldbot", "controllerbot",
    "chatkeeperbot", "grouphelpbot", "fsubbot", "missrose_bot", "rose_bot"
}

# Reklama va to'lov so'raydigan bot xabarlari kalit so'zlari
SPAM_KEYWORDS = [
    "to‘lov qilishingiz kerak",
    "to'lov qilishingiz kerak",
    "tolov qilishingiz kerak",
    "to‘lov qilish",
    "to'lov qilish",
    "tolov qilish",
    "guruhga yozish uchun to",
    "1 oy: 10 000",
    "10 000 so‘m",
    "10 000 so'm",
    "10 000 som",
    "obuna bo‘ling",
    "obuna boling",
    "kanalga a'zo",
    "kanalga azo",
    "pastdagi",
    "tugmasini bosing",
    "reklama narxi",
    "1xbet",
    "melbet",
    "mostbet",
    "linebet",
    "kazino",
    "casino",
    "pul ishlash",
    "kunlik daromad",
    "investitsiya",
    "kriptovalyuta",
    "binance",
    "virtual",
    "kartaga tashlang",
    "administratorga yozing",
]
