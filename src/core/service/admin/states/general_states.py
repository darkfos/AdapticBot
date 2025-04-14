from aiogram.fsm.state import State, StatesGroup


class CreateMeet(StatesGroup):
    user_who = State()
    user_with = State()
    description = State()
    date = State()
    time_notification = State()


class DeleteMeet(StatesGroup):
    id_meet = State()


class DeleteUser(StatesGroup):
    id_user = State()


class UpdateMeet(StatesGroup):
    id_meet = State()
    user_who = State()
    user_with = State()
    description = State()
    date = State()