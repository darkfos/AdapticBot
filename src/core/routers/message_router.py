from typing import Tuple

from aiogram import Router, types
from src.database.sqlite.repository.user_repository import UserModelRepository
from src.database.sqlite.models.user_model import UserModel

message_router: Router = Router(name="message_router")


@message_router.message()
async def message_handler(message: types.Message):

    if message.contact:
        # Сохраняем информацию о пользователе
        user_data: Tuple[UserModel] = await UserModelRepository().get_one(id_=message.from_user.id)
        user_data: UserModel = user_data[0]

        if not user_data:
            user_data: UserModel = (await UserModelRepository().find_by_phone(
                phone_number=message.contact.phone_number
            ))[0]

        if not user_data.user_phone:

            user_data.user_phone = message.contact.phone_number
            user_data.tg_id = message.from_user.id

            is_updated = await UserModelRepository().update(user_data)
            print(is_updated)

            if is_updated:
                await message.answer(
                    text=f"Отлично, {message.from_user.first_name} теперь вам доступен профиль!"
                )

            return
        await message.answer(
            text=f"Вы {message.from_user.first_name} уже подвердили свой аккаунт"
        )