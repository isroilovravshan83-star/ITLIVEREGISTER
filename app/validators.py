import re

from app.config import PHONE_OPERATOR_CODES

NAME_MIN_LEN = 2
NAME_MAX_LEN = 40
_NAME_EXTRA_CHARS = set(" -'`ʻʼ‘’")
_PHONE_JUNK = re.compile(r"[\s\-()]")


def clean_name(raw: str) -> str | None:
    """Ismni tozalaydi; noto'g'ri bo'lsa None qaytaradi."""
    name = " ".join(raw.split())
    if not NAME_MIN_LEN <= len(name) <= NAME_MAX_LEN:
        return None
    if not name[0].isalpha():
        return None
    if any(not (ch.isalpha() or ch in _NAME_EXTRA_CHARS) for ch in name):
        return None
    if sum(ch.isalpha() for ch in name) < NAME_MIN_LEN:
        return None
    return name


def normalize_phone(raw: str) -> str | None:
    """Raqamni +998XXXXXXXXX ko'rinishiga keltiradi; O'zbekiston mobil raqami bo'lmasa None."""
    phone = _PHONE_JUNK.sub("", raw)
    if phone.startswith("+"):
        phone = phone[1:]
    if not (phone.isascii() and phone.isdigit()):
        return None
    if len(phone) == 9:
        phone = "998" + phone
    if len(phone) != 12 or not phone.startswith("998"):
        return None
    if phone[3:5] not in PHONE_OPERATOR_CODES:
        return None
    return "+" + phone
