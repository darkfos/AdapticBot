from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.core.buttons.reply import ReplyButtonFabric
from src.core.service.user.states.user_states import UpdateUserPhone
from src.core.service.utils.pagination import Pagination

user_profile_router: Router = Router(name="profile_message_router")


@user_profile_router.callback_query(lambda x: x.data.startswith("profile"))
async def profile_buttons_menu(callback_data: CallbackQuery, state: FSMContext) -> None:
    """
    Обработка пользовательских сценариев из админ-панели
    """

    match callback_data.data:
        case "profile_update_phone":
            await state.set_state(UpdateUserPhone.new_user_phone)
            await callback_data.message.answer(
                text="Отлично, нажмите в нижней панели на кнопку, для отправки номера телефона",
                reply_markup=await ReplyButtonFabric.build_buttons("contact")
            )
        case "profile_meets":
            user_meets = await Pagination(int(callback_data.from_user.id)).get_meets()
            if not user_meets:
                await callback_data.message.answer(
                    text="У вас пока нет запланированных встреч"
                )
                return None

            await callback_data.message.answer(
                f"Мои встречи (страница {user_meets[-1]})\n\n"
                f"Дата: {user_meets["user_who_data"].user_name}",
                reply_markup=user_meets[1]
            )
