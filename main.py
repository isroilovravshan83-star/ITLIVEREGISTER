import asyncio
import logging
import sys
from typing import Any, Awaitable, Callable

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, TelegramObject

from app import notify, texts
from app.config import load_config
from app.db import Database
from app.handlers import get_routers


async def admin_flag_middleware(
    handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
    event: TelegramObject,
    data: dict[str, Any],
) -> Any:
    # Har handlerga `is_admin` uzatiladi (menyudagi admin tugmalari va ruxsat tekshiruvi uchun).
    user = data.get("event_from_user")
    data["is_admin"] = user is not None and user.id in data["config"].admin_ids
    return await handler(event, data)


async def main() -> None:
    config = load_config()

    db = Database(config.db_path)
    await db.init()

    bot = Bot(config.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage(), config=config, db=db)
    dp.message.outer_middleware(admin_flag_middleware)
    dp.callback_query.outer_middleware(admin_flag_middleware)
    dp.include_routers(*get_routers())

    await bot.set_my_commands([
        BotCommand(command="start", description=texts.CMD_START),
        BotCommand(command="help", description=texts.CMD_HELP),
        BotCommand(command="cancel", description=texts.CMD_CANCEL),
    ])
    await bot.delete_webhook(drop_pending_updates=False)
    await notify.check_recipients(bot, config)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        stream=sys.stdout,
    )
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot to'xtatildi")
