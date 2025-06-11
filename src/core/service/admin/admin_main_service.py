import datetime

from aiogram import Router, types, F, Bot
from aiogram.fsm.context import FSMContext

from src.core.filters.admin_filter import AdminFilter
from src.database.sqlite.repository.meet_repository import MeetModelRepository
from src.core.service.admin.states.general_states import (
    CreateMeet,
    DeleteMeet,
    UpdateMeet,
    DeleteUser,
)
from src.core.service.user.states.user_states import CreateUser
from src.core.buttons.inline import InlineButtonFabric
from src.database.sqlite.repository.user_repository import UserModelRepository
from src.database.sqlite.models.user_model import UserModel
from src.core.service.utils.pagination import Pagination
from src.database.sqlite.models.memo_model import MeetModel
from src.notifications.notifications_service import send_notification_from_admin_panel
from src.settings import TelegramBotSettings


admin_router: Router = Router(name="admin")
bot: Bot = Bot(TelegramBotSettings().telegram_bot_token)


@admin_router.callback_query(F.data == "skip")
async def skip_step(callback: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()

    if current_state == UpdateMeet.user_who.state:
        await state.update_data(user_who=None)
        await callback.message.answer(
            "Участник встречи пропущен.\nВведите данные нового сотрудника, tg_id или номер телефона следующего формата <i>79823848383</i>"
        )
        await state.set_state(UpdateMeet.user_with)
    if current_state == UpdateMeet.user_with.state:
        await state.update_data(user_with=None)
        await callback.message.answer(
            "Участник встречи пропущен.\nВведите описание встречи"
        )
        await state.set_state(UpdateMeet.description)
    if current_state == UpdateMeet.description.state:
        await state.update_data(description=None)
        await callback.message.answer(
            "Описание пропущено.\nВведите новую дату (Формат 2025-10-10 10:10:20"
        )
        await state.set_state(UpdateMeet.date)
    if current_state == CreateUser.tg_id.state:
        await state.update_data(tg_id=None)
        await callback.message.answer(
            "tg id пропущен. Введите номер телефона сотрудника, следующего формата <i>79823848383</i>"
        )
        await state.set_state(CreateUser.user_phone)


@admin_router.callback_query(lambda x: x.data.startswith("persona_"))
async def persona_menu_list(callback_data: types.CallbackQuery) -> None:
    """
    Обработка пользовательских сценариев из админ-панели
    """

    user_pagination = Pagination(int(callback_data.from_user.id))

    if callback_data.data.startswith("persona_page_next_"):
        users_data = await user_pagination.get_next(
            UserModelRepository(), int(callback_data.data.split("_")[-1])
        )
        await callback_data.message.edit_text(
            f"🧑‍⚕️ Пользователь {users_data[0].user_name}\n\n"
            f"📞  <b>Телефон: </b> {users_data[0].user_phone}\n\n"
            f"🧑‍⚕️ <b>Должность: </b> {users_data[0].post}\n\n"
            f"🪧 <b>Telegram ID: </b> {users_data[0].tg_id}\n\n"
            f"⏰ <b>Дата вступления в должность: </b> {users_data[0].date_start}",
            reply_markup=users_data[1],
        )

    if callback_data.data.startswith("persona_page_back_"):
        users_data = await user_pagination.get_previously(
            UserModelRepository(), int(callback_data.data.split("_")[-1])
        )
        await callback_data.message.edit_text(
            f"🧑‍⚕️ Пользователь {users_data[0].user_name}\n\n"
            f"📞  <b>Телефон: </b> {users_data[0].user_phone}\n\n"
            f"🧑‍⚕️ <b>Должность: </b> {users_data[0].post}\n\n"
            f"🪧 <b>Telegram ID: </b> {users_data[0].tg_id}\n\n"
            f"⏰ <b>Дата вступления в должность: </b> {users_data[0].date_start}",
            reply_markup=users_data[1],
        )


@admin_router.callback_query(AdminFilter())
async def meets_callback_handler(
    callback_data: types.CallbackQuery, state: FSMContext
) -> None:
    match callback_data.data:
        case "admin_panel_meets":
            await callback_data.message.answer(
                text="Отлично, вы выбрали опцию встречи."
            )
            meets = await MeetModelRepository().get_all()
            if len(meets) < 1:
                await callback_data.message.answer(
                    text="Запланированных встреч не нашлось."
                )
            else:
                # TODO добавить пагинацию для списка встреч
                meets_data = await Pagination().get_data(MeetModelRepository())
                await callback_data.message.answer(
                    f"📝 Встречи (страница {meets_data[-2]})\n\n"
                    f"🪧 <b>Идентификатор встречи: </b> {meets_data[0].id}\n\n"
                    f"🧑‍⚕️ <b>Кто</b>: {meets_data[0].user_who_data.user_name} ({meets_data[0].user_who_data.user_phone})\n\n"
                    f"🧑‍⚕️ <b>С кем</b>: {meets_data[0].user_with_data.user_name} ({meets_data[0].user_with_data.user_phone})\n\n"
                    f"📅  <b>Дата</b>: {meets_data[0].date_meeting}\n\n"
                    f"📑  <b>Описание встречи</b>: {meets_data[0].description[:25]}...\n\n"
                    f"📚 <b><i>Количество актуальных встреч: {meets_data[-1]}</i></b>",
                    reply_markup=meets_data[1],
                )

        case "admin_panel_create_meets":
            await callback_data.message.answer(
                text="Отлично, вы выбрали опцию создать встречу, пожалуйста заполните форму.\n\n"
                "Введите идентификатор сотрудника или его номер телефона (формат +79182348923)"
            )
            await state.set_state(state=CreateMeet.user_who)
        case "admin_panel_delete_meets":
            await callback_data.message.answer(
                text="Отлично, вы выбрали опцию удалить встречу, пожалуйста заполните форму.\n\n"
                "Введите идентификатор встречи: "
            )
            await state.set_state(DeleteMeet.id_meet)
        case "admin_panel_change_meets":
            await callback_data.message.answer(
                text="Отлично, вы выбрали опцию изменить данные о встрече, пожалуйста заполните форму.\n\n"
                "Введите идентификатор встречи: "
            )
            await state.set_state(UpdateMeet.id_meet)
        case "admin_panel_add_persona":
            await callback_data.message.answer(
                text="Добавление нового сотрудника...\n\n Пожалуйста введите <b>telegram id</b> пользователя",
                reply_markup=await InlineButtonFabric.build_buttons("skip"),
            )
            await state.set_state(state=CreateUser.tg_id)
        case "admin_panel_add_admin_persona":
            await callback_data.message.answer(
                text="Добавление нового администратора...\n\n Пожалуйста введите <b>telegram id</b> пользователя",
                reply_markup=await InlineButtonFabric.build_buttons("skip"),
            )
            await state.set_state(state=CreateUser.tg_id)
            await state.update_data({"is_admin": True})
        case "admin_panel_delete_persona":
            await callback_data.message.answer(
                text="Удаление сотрудника...\n\nПожалуйста введите <b>telegram id</b> сотрудника",
            )
            await state.set_state(DeleteUser.id_user)
        case "admin_panel_all_personal":
            data_persona = await Pagination().get_data(UserModelRepository())
            return await callback_data.message.answer(
                f"🧑‍⚕️ Пользователь {data_persona[0].user_name}\n\n"
                f"📞  <b>Телефон: </b> {data_persona[0].user_phone}\n\n"
                f"🧑‍⚕️ <b>Должность: </b> {data_persona[0].post}\n\n"
                f"🪧 <b>Telegram ID: </b> {data_persona[0].tg_id}\n\n"
                f"⏰  <b>Дата вступления в должность: </b> {data_persona[0].date_start}",
                reply_markup=data_persona[1],
            )
        case "send_notifications":
            await send_notification_from_admin_panel()

    if callback_data.data.startswith("notification"):
        try:
            message = callback_data.message

            state_data = await state.get_data()

            user_who_data = await UserModelRepository().iam_created(
                tg_id=(
                    None
                    if state_data["user_who"].startswith("+")
                    else int(state_data["user_who"])
                ),
                phone_number=(
                    state_data["user_who"][1:]
                    if state_data["user_who"].startswith("+")
                    else None
                ),
            )

            user_with_data = await UserModelRepository().iam_created(
                tg_id=(
                    None
                    if state_data["user_with"].startswith("+")
                    else int(state_data["user_with"])
                ),
                phone_number=(
                    state_data["user_with"][1:]
                    if state_data["user_with"].startswith("+")
                    else None
                ),
            )

            if user_who_data and user_with_data:

                is_added = await MeetModelRepository().create(
                    MeetModel(
                        id_who=user_who_data[0].id,
                        id_with=user_with_data[0].id,
                        description=state_data.get("description"),
                        time_format=int(callback_data.data.split("_")[-1]),
                        date_meeting=datetime.datetime.strptime(
                            state_data.get("date"), "%Y-%m-%d %H:%M:%S"
                        ),
                    )
                )

                if is_added:
                    await message.answer(text="Встреча назначена!")
            else:
                await message.answer(
                    text="Не удалось назначить встречу, не были найдены указанные сотрудники"
                )
        except Exception:
            await message.answer(
                text="Не удалось создать встречу, проверьте введенный формат даты"
            )
        finally:
            await state.clear()


# States


# ========CREATE========
@admin_router.message(CreateMeet.user_who)
async def get_user_who(message: types.Message, state: FSMContext) -> None:
    await state.update_data({"user_who": message.text})
    await message.answer(
        text="Сотрудник записан, введите идентификатор или номер телефона сотрудника кто назначает совещание (формат +79182348923)",
    )
    await state.set_state(CreateMeet.user_with)


@admin_router.message(CreateMeet.user_with)
async def get_user_with(message: types.Message, state: FSMContext) -> None:
    await state.update_data({"user_with": message.text})
    await message.answer(
        text="Сотрудник записан, введите описание ко встречи",
    )
    await state.set_state(CreateMeet.description)


@admin_router.message(CreateMeet.description)
async def get_meet_description(message: types.Message, state: FSMContext) -> None:
    await state.update_data({"description": message.text})
    await message.answer(
        text="Отлично, назначьте дату\n\nФормат 2025-10-10 10:20:00",
    )
    await state.set_state(CreateMeet.date)


@admin_router.message(CreateMeet.date)
async def get_meet_date(message: types.Message, state: FSMContext) -> None:
    await state.update_data({"date": message.text})
    await message.answer(
        text="Пожалуйста выберите формат отправки уведомлений",
        reply_markup=await InlineButtonFabric.build_buttons("notifications"),
    )


# ========DELETE========
@admin_router.message(DeleteMeet.id_meet)
async def get_id_meet(message: types.Message, state: FSMContext) -> None:
    await state.update_data({"id_meet": message.text})
    await message.answer(text="Отлично, идет обработка....")

    is_deleted = await MeetModelRepository().delete(id_=int(message.text))
    if is_deleted:
        await message.answer(text="Встреча была удалена")
    else:
        await message.answer(text="Не удалось удалить встречу")
    await state.clear()


# ========UPDATE========
@admin_router.message(UpdateMeet.id_meet)
async def get_id_meet_update_meet(message: types.Message, state: FSMContext) -> None:
    await state.update_data({"id_meet": message.text})
    await message.answer(
        text="Отлично, этап изменения участника встречи",
        reply_markup=await InlineButtonFabric.build_buttons("skip"),
    )
    await state.set_state(UpdateMeet.user_who)


@admin_router.message(UpdateMeet.user_who)
async def get_user_who_update_meet(message: types.Message, state: FSMContext) -> None:
    await state.update_data({"user_who": message.text})
    await message.answer(
        text="Отлично, этап изменения второго участника встречи",
        reply_markup=await InlineButtonFabric.build_buttons("skip"),
    )
    await state.set_state(UpdateMeet.user_with)


@admin_router.message(UpdateMeet.user_with)
async def get_user_who_update_meet(message: types.Message, state: FSMContext) -> None:
    await state.update_data({"user_with": message.text})
    await message.answer(
        text="Отлично, этап изменения описания встречи",
        reply_markup=await InlineButtonFabric.build_buttons("skip"),
    )
    await state.set_state(UpdateMeet.description)


@admin_router.message(UpdateMeet.description)
async def get_description_meet(message: types.Message, state: FSMContext) -> None:
    await state.update_data({"description": message.text})
    await message.answer(
        text="Отлично, этап изменения даты встречи",
        reply_markup=await InlineButtonFabric.build_buttons("skip"),
    )
    await state.set_state(UpdateMeet.date)


@admin_router.message(UpdateMeet.date)
async def get_date_meet(message: types.Message, state: FSMContext) -> None:
    try:
        await state.update_data({"date": message.text})
        await message.answer(text="Отлично, идет обработка...")

        meet_data = await state.get_data()
        user_who_data = None
        user_with_data = None

        if meet_data.get("user_who"):
            user_who_data = await UserModelRepository().iam_created(
                tg_id=(
                    None
                    if meet_data["user_who"].startswith("+")
                    else int(meet_data["user_who"])
                ),
                phone_number=(
                    meet_data["user_who"][1:]
                    if meet_data["user_who"].startswith("+")
                    else None
                ),
            )
        if meet_data.get("user_with"):
            user_with_data = await UserModelRepository().iam_created(
                tg_id=(
                    None
                    if meet_data["user_with"].startswith("+")
                    else int(meet_data["user_with"])
                ),
                phone_number=(
                    meet_data["user_with"][1:]
                    if meet_data["user_with"].startswith("+")
                    else None
                ),
            )

        old_meet = await MeetModelRepository().get_one(
            id_=int(meet_data.get("id_meet"))
        )

        if old_meet:
            old_meet[0].id_who = (
                user_who_data[0].id if user_who_data else old_meet[0].id_who
            )
            old_meet[0].id_with = (
                user_with_data[0].id if user_with_data else old_meet[0].id_with
            )
            old_meet[0].description = (
                meet_data.get("description")
                if meet_data.get("description")
                else old_meet[0].description
            )
            old_meet[0].date_meeting = datetime.datetime.strptime(
                meet_data.get("date"), "%Y-%m-%d %H:%M:%S"
            )
            is_updated = await MeetModelRepository().update(
                update_data_model=old_meet[0]
            )

            if is_updated:
                await message.answer("Данные встречи успешно были обновлены")
    except Exception:
        await message.answer("Не удалось обновить данные о встрече")
    finally:
        await state.clear()


# Delete User
@admin_router.message(DeleteUser.id_user)
async def delete_user(message: types.Message, state: FSMContext) -> None:
    await state.update_data({"id_user": message.text})
    is_deleted = await UserModelRepository().delete_user(int(message.text))
    if is_deleted:
        await message.answer("Пользователь был удален.")
        return
    await message.answer("Не удалось удалить пользователя")
    await state.clear()


# User
@admin_router.message(CreateUser.tg_id)
async def get_tgid_user(message: types.Message, state: FSMContext) -> None:
    await state.update_data({"tg_id": message.text})
    await message.answer(
        text="Отлично, теперь введите <b>номер телефона</b>, следующего формата <i>79823848383</i>"
    )
    await state.set_state(CreateUser.user_phone)


@admin_router.message(CreateUser.user_phone)
async def get_phone_user(message: types.Message, state: FSMContext) -> None:
    await state.update_data({"user_phone": message.text})
    await message.answer(text="Отлично, теперь введите <b>должность</b> сотрудника")
    await state.set_state(CreateUser.post)


@admin_router.message(CreateUser.post)
async def get_post_user(message: types.Message, state: FSMContext) -> None:
    await state.update_data({"post": message.text})
    await message.answer(
        text="Отлично, теперь введите <b>дату</b> вступления в должность сотрудника\n\n(Формат 2025-10-10)"
    )
    await state.set_state(CreateUser.date_start)


@admin_router.message(CreateUser.date_start)
async def get_date_user(message: types.Message, state: FSMContext) -> None:
    await state.update_data({"date_start": message.text})
    await message.answer(text="Идет обработка...")

    state_data = await state.get_data()

    try:
        user_is_created = await UserModelRepository().create(
            new_model=UserModel(
                id_user_type=2 if state_data.get("is_admin") else 1,
                user_name="Инкогнито",
                user_phone=await state.get_value("user_phone"),
                post=await state.get_value("post"),
                tg_id=await state.get_value("tg_id"),
                date_start=datetime.datetime.strptime(
                    await state.get_value("date_start"), "%Y-%m-%d"
                ),
            )
        )

        await state.clear()
        if user_is_created:
            await message.answer("Отлично, сотрудник был внесен в базу данных")
            return None

        raise Exception("Не удалось добавить пользователя")
    except Exception:
        await message.answer("Не удалось добавить сотрудника")
