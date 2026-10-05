import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import bot_config
from filter import extract_phone_numbers, is_spam_or_bot, dedup_cache, normalize_phones_in_text
from formatter import format_cargo_post

def run_tests():
    print("🧪 TEST 1: Foydalanuvchi ko'rsatgan namunadagi raqamlar (99 409 31 34)")
    sample_text = "Farg'onadan Kitobga qo'shimcha yuk bor 99 409 31 34 va +998 (91) 118-22-04 #fura #isuzu"
    phones = extract_phone_numbers(sample_text)
    print("   Aniqlangan raqamlar (Ko'k bosiladigan formatda):", phones)
    assert "+998994093134" in phones, "99 409 31 34 raqami +998994093134 ga aylanmadi"
    assert "+998911182204" in phones, "+998 (91) 118-22-04 raqami +998911182204 ga aylanmadi"
    print("   ✅ TEST 1 Muvaffaqiyatli!")

    print("\n🧪 TEST 2: Reshotkalar (#) va xunuk smayliklarni yo'qotish testi")
    formatted = format_cargo_post(
        raw_text=sample_text,
        phones=phones,
        sender_username=None,
        sender_id=12345678,
        sender_first_name="💥💥💥💥💥𒐫𒐫𒐫𒐫",
        source_title="Yuk Bozori"
    )
    assert "#" not in formatted, "Xabarda reshotka (#) qolib ketgan!"
    assert "💥💥💥💥💥" not in formatted, "Xabarda portlovchi smayliklar qolib ketgan!"
    print("   ✅ TEST 2 Muvaffaqiyatli (Reshotkalar va xunuk smayliklar 100% tozalangan)!")

    print("\n--- FORMATLANGAN POST KO'RINISHI ---")
    print(formatted)
    print("------------------------------------")
    print("\n🎉 HAMMASI A'LO DARAJADA ISHLAMOQDA!")

if __name__ == "__main__":
    run_tests()
