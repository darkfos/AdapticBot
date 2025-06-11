from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.core.buttons.reply import ReplyButtonFabric
from src.core.service.user.states.user_states import UpdateUserPhone
from src.core.service.utils.admin_filter import is_admin
from src.core.service.utils.pagination import Pagination
from src.database.sqlite.repository.meet_repository import MeetModelRepository

user_profile_router: Router = Router(name="profile_message_router")


@user_profile_router.callback_query(lambda x: x.data.startswith("profile"))
async def profile_buttons_menu(callback_data: CallbackQuery, state: FSMContext) -> None:
    """
    Обработка пользовательских сценариев из админ-панели
    """

    user_meets = Pagination(int(callback_data.from_user.id))

    match callback_data.data:
        case "profile_update_phone":
            await state.set_state(UpdateUserPhone.new_user_phone)
            await callback_data.message.answer(
                text="Отлично, нажмите в нижней панели на кнопку, для отправки номера телефона",
                reply_markup=await ReplyButtonFabric.build_buttons("contact"),
            )
        case "profile_meets":
            user_meets_data = await user_meets.get_data(MeetModelRepository())
            if not user_meets_data:
                await callback_data.message.answer(
                    text="У вас пока нет запланированных встреч"
                )
                return None

            header_message = await is_admin(int(callback_data.message.from_user.id))
            if header_message:
                await callback_data.message.answer(
                    f"📝 Встречи (страница {user_meets_data[-2]})\n\n"
                    f"🪧 <b>Идентификатор встречи: </b> {user_meets_data[0].id}\n\n"
                    f"🧑‍⚕️ <b>Кто</b>: {user_meets_data[0].user_who_data.user_name} ({user_meets_data[0].user_who_data.user_phone})\n\n"
                    f"🧑‍⚕️ <b>С кем</b>: {user_meets_data[0].user_with_data.user_name} ({user_meets_data[0].user_with_data.user_phone})\n\n"
                    f"📅 <b>Дата</b>: {user_meets_data[0].date_meeting}\n\n"
                    f"📑 <b>Описание встречи</b>: {user_meets_data[0].description[:25]}...\n\n"
                    f"📚 <b><i>Количество актуальных встреч: {user_meets_data[-1]}</i></b>",
                    reply_markup=user_meets_data[1],
                )
            else:
                await callback_data.message.answer(
                    f"📝 Мои встречи: \n\n"
                    f"🧑‍ <b>С кем</b>: {user_meets_data[0].user_who_data.user_name}\n"
                    f"📅 <b>Дата</b>: {user_meets_data[0].date_meeting}\n"
                    f"📑 <b>Описание встречи</b>: {user_meets_data[0].description[:25]}...",
                    reply_markup=user_meets_data[1],
                )

        case _:
            if "description" in callback_data.data:
                meet_data = await MeetModelRepository().get_one(
                    id_=int(callback_data.data.split("_")[-1])
                )
                if meet_data:
                    await callback_data.message.answer(
                        text="Описание: \n" + meet_data[0].description
                    )
                else:
                    await callback_data.message.answer(
                        text="Не удалось загрузить описание"
                    )
            if "next" in callback_data.data:
                user_meets_data = await user_meets.get_next(
                    MeetModelRepository(), int(callback_data.data.split("_")[-1])
                )

                header_message = await is_admin(callback_data.from_user.id)
                if header_message:
                    await callback_data.message.edit_text(
                        f"📝 Встречи (страница {user_meets_data[-2]})\n\n"
                        f"🪧 <b>Идентификатор встречи: </b> {user_meets_data[0].id}\n\n"
                        f"🧑‍⚕️ <b>Кто</b>: {user_meets_data[0].user_who_data.user_name} ({user_meets_data[0].user_who_data.user_phone})\n\n"
                        f"🧑‍⚕️ <b>С кем</b>: {user_meets_data[0].user_with_data.user_name} ({user_meets_data[0].user_with_data.user_phone})\n\n"
                        f"📅 <b>Дата</b>: {user_meets_data[0].date_meeting}\n\n"
                        f"📑 <b>Описание встречи</b>: {user_meets_data[0].description[:25]}...\n\n"
                        f"📚 <b><i>Количество актуальных встреч: {user_meets_data[-1]}</i></b>",
                        reply_markup=user_meets_data[1],
                    )
                else:
                    await callback_data.message.edit_text(
                        f"📝 Мои встречи: \n\n"
                        f"🧑‍ <b>С кем</b>: {user_meets_data[0].user_who_data.user_name}\n"
                        f"📅 <b>Дата</b>: {user_meets_data[0].date_meeting}\n"
                        f"📑 <b>Описание встречи</b>: {user_meets_data[0].description[:25]}...",
                        reply_markup=user_meets_data[1],
                    )

            elif "back" in callback_data.data:
                user_meets_data = await user_meets.get_previously(
                    MeetModelRepository(), int(callback_data.data.split("_")[-1])
                )

                header_message = await is_admin(callback_data.from_user.id)
                if header_message:
                    await callback_data.message.edit_text(
                        f"📝 Встречи (страница {user_meets_data[-2]})\n\n"
                        f"🪧 <b>Идентификатор встречи: </b> {user_meets_data[0].id}\n\n"
                        f"🧑‍⚕️ <b>Кто</b>: {user_meets_data[0].user_who_data.user_name} ({user_meets_data[0].user_who_data.user_phone})\n\n"
                        f"🧑‍⚕️ <b>С кем</b>: {user_meets_data[0].user_with_data.user_name} ({user_meets_data[0].user_with_data.user_phone})\n\n"
                        f"📅 <b>Дата</b>: {user_meets_data[0].date_meeting}\n\n"
                        f"📑 <b>Описание встречи</b>: {user_meets_data[0].description[:25]}...\n\n"
                        f"📚 <b><i>Количество актуальных встреч: {user_meets_data[-1]}</i></b>",
                        reply_markup=user_meets_data[1],
                    )
                else:
                    await callback_data.message.edit_text(
                        f"📝 Мои встречи: \n\n"
                        f"🧑‍ <b>С кем</b>: {user_meets_data[0].user_who_data.user_name}\n"
                        f"📅 <b>Дата</b>: {user_meets_data[0].date_meeting}\n"
                        f"📑 <b>Описание встречи</b>: {user_meets_data[0].description[:25]}...",
                        reply_markup=user_meets_data[1],
                    )
