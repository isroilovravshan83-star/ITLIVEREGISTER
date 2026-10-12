import os
from dataclasses import dataclass
from datetime import timedelta, timezone

from dotenv import load_dotenv

load_dotenv()

# O'zbekistonda yozgi vaqt yo'q, shuning uchun Asia/Tashkent = doimiy UTC+5.
# zoneinfo Windows'da qo'shimcha tzdata paketini talab qiladi — undan qochamiz.
TZ = timezone(timedelta(hours=5), name="Asia/Tashkent")

# Aloqa ma'lumotlari (sir emas). Koordinatalar None bo'lsa, lokatsiya yuborilmaydi.
CONTACT_PHONE = "+998872848060"
CONTACT_ADDRESS = "Xalqlar do'stligi ko'chasi, yangi prokuratura ro'parasi"
CONTACT_LANDMARK = "Eski muzey"
CONTACT_HOURS = "8:00 – 18:00"
CONTACT_LAT: float | None = None
CONTACT_LON: float | None = None

# O'zbekiston mobil operator kodlari (+998 dan keyingi 2 raqam). Yangi kod chiqsa — shu yerga qo'shiladi.
PHONE_OPERATOR_CODES = frozenset({
    "20", "33", "50", "55", "77", "88", "90", "91", "93", "94", "95", "97", "98", "99",
})


@dataclass(frozen=True)
class Config:
    bot_token: str
    admin_ids: frozenset[int]
    admin_chat_id: int | None
    manager_ids: tuple[int, ...]
    db_path: str


def _parse_ids(name: str) -> tuple[int, ...]:
    raw = os.getenv(name, "")
    try:
        return tuple(int(part) for part in raw.replace(" ", "").split(",") if part)
    except ValueError:
        raise SystemExit(f"{name} faqat vergul bilan ajratilgan raqamlardan iborat bo'lishi kerak")


def load_config() -> Config:
    token = os.getenv("BOT_TOKEN", "").strip()
    if not token:
        raise SystemExit("BOT_TOKEN .env faylida ko'rsatilmagan")

    admin_chat = _parse_ids("ADMIN_CHAT_ID")

    return Config(
        bot_token=token,
        admin_ids=frozenset(_parse_ids("ADMIN_IDS")),
        admin_chat_id=admin_chat[0] if admin_chat else None,
        manager_ids=_parse_ids("MANAGER_IDS"),
        db_path=os.getenv("DB_PATH", "").strip() or "data/bot.db",
    )
