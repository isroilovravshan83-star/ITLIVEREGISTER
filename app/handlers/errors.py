import logging

from aiogram import Router
from aiogram.exceptions import TelegramAPIError
from aiogram.types import ErrorEvent

logger = logging.getLogger(__name__)

router = Router(name="errors")


@router.errors()
async def on_error(event: ErrorEvent) -> bool:
    # Xato log'ga yoziladi, polling esa to'xtamaydi.
    logger.exception("Update %s ni qayta ishlashda xato", event.update.update_id, exc_info=event.exception)
    # Tugmadagi "soat" belgisi aylanib qolmasin.
    if event.update.callback_query is not None:
        try:
            await event.update.callback_query.answer()
        except TelegramAPIError:
            pass
    return True
