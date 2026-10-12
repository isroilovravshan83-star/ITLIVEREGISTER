from aiogram import Router

from app.handlers import admin, apply, common, contact, errors, fallback, manager


def get_routers() -> list[Router]:
    # Tartib muhim: common (start/cancel) birinchi, fallback oxirida.
    return [
        errors.router,
        common.router,
        admin.router,
        manager.router,
        apply.router,
        contact.router,
        fallback.router,
    ]
