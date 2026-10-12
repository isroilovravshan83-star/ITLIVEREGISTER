from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

from app import texts


class LeadAction(CallbackData, prefix="lead"):
    lead_id: int
    status: str  # o'rnatiladigan status: accepted / talked / callback / informed / unreachable


def _cancel_row() -> list[KeyboardButton]:
    return [KeyboardButton(text=texts.BTN_CANCEL)]


def main_menu(is_admin: bool = False) -> ReplyKeyboardMarkup:
    rows = [
        [KeyboardButton(text=texts.BTN_APPLY)],
        [KeyboardButton(text=texts.BTN_CONTACT)],
    ]
    if is_admin:
        rows.append([KeyboardButton(text=texts.BTN_STATS), KeyboardButton(text=texts.BTN_EXPORT)])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def lead_card(lead_id: int, status: str) -> InlineKeyboardMarkup:
    if status == "new":
        return InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(
                text=texts.BTN_ACCEPT,
                callback_data=LeadAction(lead_id=lead_id, status="accepted").pack(),
            ),
        ]])
    buttons = [
        InlineKeyboardButton(
            text=("• " if code == status else "") + texts.STATUSES[code],
            callback_data=LeadAction(lead_id=lead_id, status=code).pack(),
        )
        for code in texts.RESULT_STATUSES
    ]
    return InlineKeyboardMarkup(inline_keyboard=[buttons[:2], buttons[2:]])


def cancel_only() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(keyboard=[_cancel_row()], resize_keyboard=True)


def send_phone() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=texts.BTN_SEND_PHONE, request_contact=True)],
            _cancel_row(),
        ],
        resize_keyboard=True,
    )


def options(labels: dict[str, str], per_row: int = 2) -> ReplyKeyboardMarkup:
    values = list(labels.values())
    rows = [[KeyboardButton(text=v) for v in values[i:i + per_row]] for i in range(0, len(values), per_row)]
    rows.append(_cancel_row())
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def confirm() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=texts.BTN_CONFIRM)],
            [KeyboardButton(text=texts.BTN_RESTART)],
            _cancel_row(),
        ],
        resize_keyboard=True,
    )
