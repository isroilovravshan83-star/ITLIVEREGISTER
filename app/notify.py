import logging
from dataclasses import replace
from datetime import datetime

from aiogram import Bot, html
from aiogram.enums import ChatAction
from aiogram.exceptions import TelegramAPIError, TelegramBadRequest, TelegramForbiddenError
from aiogram.types import InlineKeyboardMarkup, Message

from app import keyboards, texts
from app.config import TZ, Config
from app.db import Database, Lead

logger = logging.getLogger(__name__)


def format_dt(dt: datetime) -> str:
    return dt.astimezone(TZ).strftime("%d.%m.%Y %H:%M")


def render_card(lead: Lead) -> str:
    telegram = f"@{lead.tg_username}" if lead.tg_username else texts.PROFILE_LINK.format(id=lead.tg_id)
    text = texts.CARD.format(
        id=lead.id,
        name=html.quote(lead.name),
        phone=lead.phone,
        phone_source=texts.PHONE_SOURCES[lead.phone_source],
        course=texts.COURSES[lead.course],
        study_format=texts.FORMATS[lead.study_format],
        pref_time=texts.PREF_TIMES[lead.pref_time],
        telegram=telegram,
        created=format_dt(lead.created_at),
        status=texts.STATUSES[lead.status],
    )
    if lead.manager_id is None:
        text += texts.CARD_NOT_DELIVERED
    elif lead.accepted_at is not None:
        text += texts.CARD_MANAGER.format(
            manager=texts.PROFILE_LINK.format(id=lead.manager_id),
            accepted=format_dt(lead.accepted_at),
        )
    return text


async def _send(bot: Bot, chat_id: int, text: str, markup: InlineKeyboardMarkup) -> Message | None:
    try:
        return await bot.send_message(chat_id, text, reply_markup=markup)
    except TelegramForbiddenError:
        logger.warning("Chat %s botni bloklagan yoki /start bosmagan", chat_id)
    except TelegramAPIError as exc:
        logger.warning("Chat %s ga yuborib bo'lmadi: %s", chat_id, exc)
    return None


async def dispatch_new_lead(bot: Bot, db: Database, config: Config, lead_id: int) -> None:
    """Arizani navbatdagi menejerga yuboradi (yetmasa — keyingisiga) va nusxasini admin chatiga."""
    lead = await db.get_lead(lead_id)
    managers = config.manager_ids
    markup = keyboards.lead_card(lead.id, lead.status)

    manager_id = manager_msg_id = next_index = None
    start = await db.get_rr_index() if managers else 0
    for offset in range(len(managers)):
        index = (start + offset) % len(managers)
        candidate = managers[index]
        sent = await _send(bot, candidate, render_card(replace(lead, manager_id=candidate)), markup)
        if sent is not None:
            manager_id, manager_msg_id = candidate, sent.message_id
            next_index = (index + 1) % len(managers)
            break

    lead = replace(lead, manager_id=manager_id)
    admin_msg_id = None
    # Admin chati menejer chati bilan bir xil bo'lsa, ikkinchi nusxa yuborilmaydi.
    if config.admin_chat_id is not None and config.admin_chat_id != manager_id:
        sent = await _send(bot, config.admin_chat_id, render_card(lead), markup)
        admin_msg_id = sent.message_id if sent else None

    await db.set_delivery(
        lead.id,
        manager_id=manager_id,
        manager_msg_id=manager_msg_id,
        admin_msg_id=admin_msg_id,
        rr_index=next_index,
    )
    if manager_id is None and admin_msg_id is None:
        logger.error("Ariza #%s hech kimga yetkazilmadi (MANAGER_IDS / ADMIN_CHAT_ID ni tekshiring)", lead.id)
    else:
        logger.info("Ariza #%s yuborildi: menejer=%s, admin nusxa=%s", lead.id, manager_id, admin_msg_id is not None)


async def refresh_cards(bot: Bot, config: Config, lead: Lead) -> None:
    """Menejer va admin chatidagi kartani bazadagi joriy holatga keltiradi."""
    text = render_card(lead)
    markup = keyboards.lead_card(lead.id, lead.status)
    for chat_id, message_id in ((lead.manager_id, lead.manager_msg_id), (config.admin_chat_id, lead.admin_msg_id)):
        if chat_id is None or message_id is None:
            continue
        try:
            await bot.edit_message_text(text=text, chat_id=chat_id, message_id=message_id, reply_markup=markup)
        except TelegramBadRequest as exc:
            if "message is not modified" not in str(exc):
                logger.warning("Karta #%s ni chat %s da yangilab bo'lmadi: %s", lead.id, chat_id, exc)
        except TelegramAPIError as exc:
            logger.warning("Karta #%s ni chat %s da yangilab bo'lmadi: %s", lead.id, chat_id, exc)


async def notify_user(bot: Bot, lead: Lead) -> None:
    try:
        await bot.send_message(lead.tg_id, texts.USER_STATUS[lead.status].format(id=lead.id))
    except TelegramForbiddenError:
        logger.info("Ariza #%s egasi botni bloklagan — status xabari yuborilmadi", lead.id)
    except TelegramAPIError as exc:
        logger.warning("Ariza #%s egasiga status xabari yuborilmadi: %s", lead.id, exc)


async def check_recipients(bot: Bot, config: Config) -> None:
    """Ishga tushganda: menejerlarga xabar yetib borishini tekshiradi, muammo bo'lsa adminga yozadi."""
    if not config.manager_ids:
        logger.warning("MANAGER_IDS bo'sh — arizalar faqat admin chatiga boradi")
    if config.admin_chat_id is None:
        logger.warning("ADMIN_CHAT_ID ko'rsatilmagan — adminlarga ariza nusxasi bormaydi")

    unreachable = []
    for manager_id in config.manager_ids:
        try:
            await bot.send_chat_action(manager_id, ChatAction.TYPING)
        except TelegramAPIError:
            unreachable.append(manager_id)
    if not unreachable:
        return
    ids = ", ".join(map(str, unreachable))
    logger.warning("Menejerlarga yetib bo'lmayapti: %s", ids)
    if config.admin_chat_id is not None:
        try:
            await bot.send_message(config.admin_chat_id, texts.RECIPIENT_UNREACHABLE.format(ids=ids))
        except TelegramAPIError as exc:
            logger.warning("Admin chatiga ogohlantirish yuborilmadi: %s", exc)
