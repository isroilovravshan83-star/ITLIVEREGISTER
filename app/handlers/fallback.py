from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.types import Message

from app import keyboards, texts

# Oxirgi bo'lib ulanadi: boshqa hech bir handler tutmagan xabarlar shu yerga tushadi.
router = Router(name="fallback")
router.message.filter(F.chat.type == ChatType.PRIVATE)


@router.message()
async def unknown_message(message: Message, is_admin: bool) -> None:
    await message.answer(texts.UNKNOWN, reply_markup=keyboards.main_menu(is_admin))
