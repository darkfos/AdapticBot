from aiogram.fsm.state import State, StatesGroup


class CreateUser(StatesGroup):
    tg_id = State()
    user_phone = State()
    post = State()
    date_start = State()


class UpdateUserPhone(StatesGroup):
    new_user_phone = State()