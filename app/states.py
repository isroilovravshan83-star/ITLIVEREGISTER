from aiogram.fsm.state import State, StatesGroup


class ApplyForm(StatesGroup):
    name = State()
    phone = State()
    course = State()
    study_format = State()
    pref_time = State()
    confirm = State()
