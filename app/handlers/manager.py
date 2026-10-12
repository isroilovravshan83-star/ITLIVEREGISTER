from aiogram import Bot, Router
from aiogram.types import CallbackQuery

from app import notify, texts
from app.config import Config
from app.db import Database
from app.keyboards import LeadAction

# Kartadagi inline tugmalar. Admin chati guruh bo'lishi mumkin, shuning uchun chat turi cheklanmaydi.
router = Router(name="manager")


def _is_allowed_transition(current: str, new: str) -> bool:
    if current == "new":
        return new == "accepted"
    return new in texts.RESULT_STATUSES and new != current


@router.callback_query(LeadAction.filter())
async def on_lead_action(
    callback: CallbackQuery,
    callback_data: LeadAction,
    bot: Bot,
    db: Database,
    config: Config,
) -> None:
    lead = await db.get_lead(callback_data.lead_id)
    if lead is None:
        await callback.answer(texts.CB_NOT_FOUND, show_alert=True)
        return

    user_id = callback.from_user.id
    if user_id not in config.admin_ids and user_id != lead.manager_id:
        await callback.answer(texts.NO_ACCESS, show_alert=True)
        return

    new = callback_data.status
    if not _is_allowed_transition(lead.status, new) or not await db.change_status(lead.id, lead.status, new, user_id):
        # Eski karta yoki boshqa odam allaqachon o'zgartirgan — kartani joriy holatga keltiramiz.
        await notify.refresh_cards(bot, config, await db.get_lead(lead.id))
        await callback.answer(texts.CB_ALREADY)
        return

    lead = await db.get_lead(lead.id)
    await callback.answer(
        texts.CB_ACCEPTED if new == "accepted" else texts.CB_STATUS_SET.format(status=texts.STATUSES[new])
    )
    await notify.refresh_cards(bot, config, lead)
    await notify.notify_user(bot, lead)
