from typing import Tuple

from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from src.database.sqlite.repository.user_repository import UserModelRepository
from src.database.sqlite.models.user_model import UserModel

message_router: Router = Router(name="message_router")


@message_router.message()
async def message_handler(message: types.Message, state: FSMContext):

    if message.contact:

        # Сохраняем информацию о пользователе
        user_data: Tuple[UserModel] = await UserModelRepository().get_one(id_=message.from_user.id)

        if user_data:
            user_data = user_data[0]

        if not user_data:
            user_data: UserModel = (await UserModelRepository().find_by_phone(
                phone_number=message.contact.phone_number
            ))[0]

        if user_data:

            user_data.user_phone = message.contact.phone_number
            user_data.tg_id = message.from_user.id
            user_data.user_name = message.from_user.first_name

            is_updated = await UserModelRepository().update(user_data)

            if is_updated:
                await message.answer(
                    text="Отлично, номер телефона был обновлен!"
                )
                return

            await message.answer(
                text="Не удалось обновить ваш номер телефона"
            )

        if not user_data.user_phone or not user_data.tg_id:

            user_data.user_phone = message.contact.phone_number
            user_data.tg_id = message.from_user.id

            is_updated = await UserModelRepository().update(user_data)

            if is_updated:
                if state.get_value("new_user_phone"):
                    await message.answer(
                        text="Отлично, номер телефона был обновлен!"
                    )
                else:
                    await message.answer(
                        text=f"Отлично, {message.from_user.first_name} теперь вам доступен профиль!"
                    )

            return

        await message.answer(
            text=f"Вы {message.from_user.first_name} уже подвердили свой аккаунт"
        )