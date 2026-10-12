from aiogram import F, Router, html
from aiogram.enums import ChatType
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app import keyboards, texts

router = Router(name="common")
router.message.filter(F.chat.type == ChatType.PRIVATE)


@router.message(CommandStart(), StateFilter("*"))
async def cmd_start(message: Message, state: FSMContext, is_admin: bool) -> None:
    await state.clear()
    await message.answer(
        texts.START.format(first_name=html.quote(message.from_user.first_name)),
        reply_markup=keyboards.main_menu(is_admin),
    )


@router.message(Command("help"), StateFilter("*"))
async def cmd_help(message: Message, is_admin: bool) -> None:
    await message.answer(texts.HELP + (texts.HELP_ADMIN if is_admin else ""))


@router.message(Command("cancel"), StateFilter("*"))
@router.message(F.text == texts.BTN_CANCEL, StateFilter("*"))
async def cmd_cancel(message: Message, state: FSMContext, is_admin: bool) -> None:
    if await state.get_state() is None:
        await message.answer(texts.NOTHING_TO_CANCEL, reply_markup=keyboards.main_menu(is_admin))
        return
    await state.clear()
    await message.answer(texts.CANCELLED, reply_markup=keyboards.main_menu(is_admin))
