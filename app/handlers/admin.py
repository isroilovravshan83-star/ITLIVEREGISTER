import csv
import io
from datetime import datetime, timedelta, timezone

from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.filters import Command, StateFilter, or_f
from aiogram.types import BufferedInputFile, Message

from app import texts
from app.config import TZ
from app.db import Database
from app.notify import format_dt

router = Router(name="admin")
router.message.filter(F.chat.type == ChatType.PRIVATE)


def _plain(label: str) -> str:
    """Tugma yozuvidan emoji'ni olib tashlaydi: '💻 Frontend' → 'Frontend'."""
    return label.split(" ", 1)[1]


def _pretty_phone(phone: str) -> str:
    # Bo'sh joyli ko'rinish Excel'da matn bo'lib qoladi (aks holda raqamni 9.98901E+11 qilib buzadi).
    return f"{phone[:4]} {phone[4:6]} {phone[6:9]} {phone[9:11]} {phone[11:]}"


def _format_minutes(minutes: float | None) -> str:
    if minutes is None:
        return texts.STATS_NO_DATA
    minutes = round(minutes)
    if minutes < 60:
        return f"{minutes} daq"
    return f"{minutes // 60} soat {minutes % 60} daq"


def _breakdown(labels: dict[str, str], counts: dict[str, int]) -> str:
    return "\n".join(f"{label}: {counts.get(code, 0)}" for code, label in labels.items())


@router.message(or_f(Command("stats"), F.text == texts.BTN_STATS), StateFilter("*"))
async def cmd_stats(message: Message, db: Database, is_admin: bool) -> None:
    if not is_admin:
        await message.answer(texts.NO_ACCESS)
        return

    now = datetime.now(TZ)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0).astimezone(timezone.utc)
    week_start = (now - timedelta(days=7)).astimezone(timezone.utc)
    data = await db.stats(today_start.isoformat(timespec="seconds"), week_start.isoformat(timespec="seconds"))
    if data["total"] == 0:
        await message.answer(texts.NO_LEADS)
        return

    await message.answer(texts.STATS.format(
        today=data["today"],
        week=data["week"],
        total=data["total"],
        by_status=_breakdown(texts.STATUSES, data["status"]),
        by_course=_breakdown(texts.COURSES, data["course"]),
        by_format=_breakdown(texts.FORMATS, data["study_format"]),
        avg_accept=_format_minutes(data["avg_accept_min"]),
    ))


@router.message(or_f(Command("export"), F.text == texts.BTN_EXPORT), StateFilter("*"))
async def cmd_export(message: Message, db: Database, is_admin: bool) -> None:
    if not is_admin:
        await message.answer(texts.NO_ACCESS)
        return

    leads = await db.all_leads()
    if not leads:
        await message.answer(texts.NO_LEADS)
        return

    buffer = io.StringIO()
    writer = csv.writer(buffer, delimiter=";")
    writer.writerow(texts.EXPORT_HEADER)
    for lead in leads:
        writer.writerow([
            lead.id,
            format_dt(lead.created_at),
            lead.name,
            _pretty_phone(lead.phone),
            _plain(texts.COURSES[lead.course]),
            _plain(texts.FORMATS[lead.study_format]),
            _plain(texts.PREF_TIMES[lead.pref_time]),
            _plain(texts.STATUSES[lead.status]),
            lead.manager_id or "",
            format_dt(lead.accepted_at) if lead.accepted_at else "",
            f"@{lead.tg_username}" if lead.tg_username else "",
        ])

    filename = f"itlive_arizalar_{datetime.now(TZ):%Y-%m-%d}.csv"
    await message.answer_document(
        BufferedInputFile(buffer.getvalue().encode("utf-8-sig"), filename=filename),
        caption=texts.EXPORT_DONE.format(count=len(leads)),
    )
