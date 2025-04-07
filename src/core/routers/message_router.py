from typing import Tuple

from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

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
                phone_number=message.contact.phone_number[1:]
            ))

        if user_data:

            user_data[0].user_phone = message.contact.phone_number[1:]
            user_data[0].tg_id = message.from_user.id
            user_data[0].user_name = message.from_user.first_name

            is_updated = await UserModelRepository().update(user_data[0])

            if is_updated:
                await message.answer(
                    text="Отлично, номер телефона был обновлен!",
                    reply_markup=ReplyKeyboardRemove()
                )
                return

            await message.answer(
                text="Не удалось обновить ваш номер телефона",
                reply_markup=ReplyKeyboardRemove()
            )

        if not user_data.user_phone or not user_data.tg_id:

            user_data[0].user_phone = message.contact.phone_number[1:]
            user_data[0].tg_id = message.from_user.id

            is_updated = await UserModelRepository().update(user_data[0])

            if is_updated:
                if state.get_value("new_user_phone"):
                    await message.answer(
                        text="Отлично, номер телефона был обновлен!",
                        reply_markup=ReplyKeyboardRemove()
                    )
                else:
                    await message.answer(
                        text=f"Отлично, {message.from_user.first_name} теперь вам доступен профиль!",
                        reply_markup=ReplyKeyboardRemove()
                    )

            return

        await message.answer(
            text=f"Вы {message.from_user.first_name} уже подвердили свой аккаунт",
            reply_markup=ReplyKeyboardRemove()
        )