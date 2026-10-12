from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.filters import StateFilter
from aiogram.types import Message

from app import config, keyboards, texts

router = Router(name="contact")
router.message.filter(F.chat.type == ChatType.PRIVATE)


@router.message(StateFilter(None), F.text == texts.BTN_CONTACT)
async def show_contact(message: Message, is_admin: bool) -> None:
    await message.answer(
        texts.CONTACT.format(
            phone=config.CONTACT_PHONE,
            address=config.CONTACT_ADDRESS,
            landmark=config.CONTACT_LANDMARK,
            hours=config.CONTACT_HOURS,
        ),
        reply_markup=keyboards.main_menu(is_admin),
    )
    if config.CONTACT_LAT is not None and config.CONTACT_LON is not None:
        await message.answer_venue(
            latitude=config.CONTACT_LAT,
            longitude=config.CONTACT_LON,
            title=texts.VENUE_TITLE,
            address=config.CONTACT_ADDRESS,
        )
