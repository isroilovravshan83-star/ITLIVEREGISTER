import logging
from datetime import datetime

from aiogram import Bot, F, Router, html
from aiogram.enums import ChatType
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup

from app import keyboards, notify, texts
from app.config import TZ, Config
from app.db import Database, DuplicateLeadError
from app.states import ApplyForm
from app.validators import clean_name, normalize_phone

logger = logging.getLogger(__name__)

router = Router(name="apply")
router.message.filter(F.chat.type == ChatType.PRIVATE)


def _code_by_label(labels: dict[str, str], label: str) -> str:
    return next(code for code, text in labels.items() if text == label)


def _local_date(dt: datetime) -> str:
    return dt.astimezone(TZ).strftime("%d.%m.%Y")


async def _ask_name(message: Message, state: FSMContext) -> None:
    await state.set_data({})
    await state.set_state(ApplyForm.name)
    await message.answer(texts.ASK_NAME, reply_markup=keyboards.cancel_only())


@router.message(StateFilter(None), F.text == texts.BTN_APPLY)
async def start_apply(message: Message, state: FSMContext, db: Database, is_admin: bool) -> None:
    lead = await db.get_lead_by_tg(message.from_user.id)
    if lead is not None:
        await message.answer(
            texts.ALREADY_APPLIED.format(id=lead.id, date=_local_date(lead.created_at)),
            reply_markup=keyboards.main_menu(is_admin),
        )
        return
    await _ask_name(message, state)


@router.message(ApplyForm.name, F.text)
async def got_name(message: Message, state: FSMContext) -> None:
    name = clean_name(message.text)
    if name is None:
        await message.answer(texts.ERR_NAME, reply_markup=keyboards.cancel_only())
        return
    await state.update_data(name=name)
    await state.set_state(ApplyForm.phone)
    await message.answer(texts.ASK_PHONE, reply_markup=keyboards.send_phone())


async def _save_phone(
    message: Message, state: FSMContext, db: Database, is_admin: bool, raw: str, source: str
) -> None:
    phone = normalize_phone(raw)
    if phone is None:
        await message.answer(texts.ERR_PHONE, reply_markup=keyboards.send_phone())
        return
    if await db.phone_exists(phone):
        await state.clear()
        await message.answer(texts.PHONE_TAKEN, reply_markup=keyboards.main_menu(is_admin))
        return
    await state.update_data(phone=phone, phone_source=source)
    await state.set_state(ApplyForm.course)
    await message.answer(texts.ASK_COURSE, reply_markup=keyboards.options(texts.COURSES))


@router.message(ApplyForm.phone, F.contact)
async def got_contact(message: Message, state: FSMContext, db: Database, is_admin: bool) -> None:
    if message.contact.user_id != message.from_user.id:
        await message.answer(texts.ERR_FOREIGN_CONTACT, reply_markup=keyboards.send_phone())
        return
    await _save_phone(message, state, db, is_admin, message.contact.phone_number, "contact")


@router.message(ApplyForm.phone, F.text)
async def got_phone_text(message: Message, state: FSMContext, db: Database, is_admin: bool) -> None:
    await _save_phone(message, state, db, is_admin, message.text, "typed")


@router.message(ApplyForm.course, F.text.in_(texts.COURSES.values()))
async def got_course(message: Message, state: FSMContext) -> None:
    await state.update_data(course=_code_by_label(texts.COURSES, message.text))
    await state.set_state(ApplyForm.study_format)
    await message.answer(texts.ASK_FORMAT, reply_markup=keyboards.options(texts.FORMATS))


@router.message(ApplyForm.study_format, F.text.in_(texts.FORMATS.values()))
async def got_format(message: Message, state: FSMContext) -> None:
    await state.update_data(study_format=_code_by_label(texts.FORMATS, message.text))
    await state.set_state(ApplyForm.pref_time)
    await message.answer(texts.ASK_TIME, reply_markup=keyboards.options(texts.PREF_TIMES, per_row=1))


@router.message(ApplyForm.pref_time, F.text.in_(texts.PREF_TIMES.values()))
async def got_time(message: Message, state: FSMContext) -> None:
    data = await state.update_data(pref_time=_code_by_label(texts.PREF_TIMES, message.text))
    await state.set_state(ApplyForm.confirm)
    await message.answer(
        texts.CONFIRM.format(
            name=html.quote(data["name"]),
            phone=data["phone"],
            course=texts.COURSES[data["course"]],
            study_format=texts.FORMATS[data["study_format"]],
            pref_time=texts.PREF_TIMES[data["pref_time"]],
        ),
        reply_markup=keyboards.confirm(),
    )


@router.message(ApplyForm.confirm, F.text == texts.BTN_CONFIRM)
async def confirmed(
    message: Message, state: FSMContext, bot: Bot, db: Database, config: Config, is_admin: bool
) -> None:
    data = await state.get_data()
    await state.clear()
    try:
        lead_id = await db.create_lead(
            tg_id=message.from_user.id,
            tg_username=message.from_user.username,
            name=data["name"],
            phone=data["phone"],
            phone_source=data["phone_source"],
            course=data["course"],
            study_format=data["study_format"],
            pref_time=data["pref_time"],
        )
    except DuplicateLeadError:
        lead = await db.get_lead_by_tg(message.from_user.id)
        text = (
            texts.ALREADY_APPLIED.format(id=lead.id, date=_local_date(lead.created_at))
            if lead is not None else texts.PHONE_TAKEN
        )
        await message.answer(text, reply_markup=keyboards.main_menu(is_admin))
        return
    await message.answer(
        texts.APPLIED.format(id=lead_id, pref_time=texts.PREF_TIMES[data["pref_time"]]),
        reply_markup=keyboards.main_menu(is_admin),
    )
    # Ariza bazada saqlangan; yuborishdagi xato foydalanuvchiga ta'sir qilmasin.
    try:
        await notify.dispatch_new_lead(bot, db, config, lead_id)
    except Exception:
        logger.exception("Ariza #%s ni menejerga yuborishda xato", lead_id)


@router.message(ApplyForm.confirm, F.text == texts.BTN_RESTART)
async def restart(message: Message, state: FSMContext) -> None:
    await _ask_name(message, state)


_STATE_KEYBOARDS = {
    ApplyForm.name.state: keyboards.cancel_only,
    ApplyForm.phone.state: keyboards.send_phone,
    ApplyForm.course.state: lambda: keyboards.options(texts.COURSES),
    ApplyForm.study_format.state: lambda: keyboards.options(texts.FORMATS),
    ApplyForm.pref_time.state: lambda: keyboards.options(texts.PREF_TIMES, per_row=1),
    ApplyForm.confirm.state: keyboards.confirm,
}


# Formadagi istalgan qadamda kutilmagan kiritish (noto'g'ri matn, stiker, rasm, ovoz):
# dialog buzilmaydi, o'sha qadam klaviaturasi bilan qayta so'raladi.
@router.message(StateFilter(ApplyForm))
async def wrong_input(message: Message, state: FSMContext) -> None:
    keyboard: ReplyKeyboardMarkup = _STATE_KEYBOARDS[await state.get_state()]()
    await message.answer(texts.ERR_BUTTON if message.text else texts.ERR_MEDIA, reply_markup=keyboard)
