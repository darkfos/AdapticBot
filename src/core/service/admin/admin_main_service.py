import datetime

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from src.core.filters.admin_filter import AdminFilter
from src.database.sqlite.repository.meet_repository import MeetModelRepository
from src.core.service.admin.states.general_states import CreateMeet, DeleteMeet, UpdateMeet
from src.core.service.user.states.user_states import CreateUser
from src.core.buttons.inline import InlineButtonFabric
from src.database.sqlite.repository.user_repository import UserModelRepository
from src.database.sqlite.models.user_model import UserModel

admin_router: Router = Router(name="admin")


@admin_router.callback_query(F.data == "skip")
async def skip_step(callback: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()

    if current_state == UpdateMeet.user_who.state:
        await state.update_data(user_who=None)
        await callback.message.answer("Участник пропущен. Введите второго участника:")
        await state.set_state(UpdateMeet.user_with)

    elif current_state == UpdateMeet.user_with.state:
        await state.update_data(user_with=None)
        await callback.message.answer("Второй участник пропущен. Введите описание:")
        await state.set_state(UpdateMeet.description)

    elif current_state == UpdateMeet.description.state:
        await state.update_data(description=None)
        await callback.message.answer("Описание пропущено. Введите новую дату:")
        await state.set_state(UpdateMeet.date)
    elif current_state == CreateUser.tg_id.state:
        await state.update_data(tg_id=None)
        await callback.message.answer("tg id пропущен. Введите номер телефона сотрудника, следующего формата <i>79823848383</i>")
        await state.set_state(CreateUser.user_phone)


@admin_router.callback_query(AdminFilter())
async def meets_callback_handler(message: types.CallbackQuery, state: FSMContext) -> None:
    match message.data:
        case "admin_panel_meets":
            await message.message.answer(text="Отлично, вы выбрали опцию встречи.")
            meets = await MeetModelRepository().get_all()
            if len(meets) < 1:
                await message.message.answer(text="Запланированных встреч не нашлось.")
            else:
                # TODO добавить пагинацию для списка встреч
                pass
        case "admin_panel_create_meets":
            await message.message.answer(text="Отлично, вы выбрали опцию создать встречу, пожалуйста заполните форму.\n\n"
                                              "Введите идентификатор сотрудника или его номер телефона")
            await state.set_state(state=CreateMeet.user_who)
        case "admin_panel_delete_meets":
            await message.message.answer(text="Отлично, вы выбрали опцию удалить встречу, пожалуйста заполните форму.\n\n"
                                              "Введите идентификатор встречи: ")
            await state.set_state(DeleteMeet.id_meet)
        case "admin_panel_change_meets":
            await message.message.answer(text="Отлично, вы выбрали опцию изменить данные о встрече, пожалуйста заполните форму.\n\n"
                                              "Введите идентификатор встречи: ")
            await state.set_state(UpdateMeet.id_meet)
        case "add_persona":
            await message.message.answer(
                text="Добавление нового сотрудника...\n\n Пожалуйста введите <b>telegram id</b> пользователя",
                reply_markup=await InlineButtonFabric.build_buttons("skip")
            )
            await state.set_state(state=CreateUser.tg_id)

# States

# ========CREATE========
@admin_router.message(CreateMeet.user_who)
async def get_user_who(message: types.Message, state: FSMContext) -> None:
    await state.update_data({"user_who": message.text})
    await message.answer(
        text="Сотрудник записан, введите идентификатор или номер сотрудника (ментор, HRD)",
    )
    await state.set_state(CreateMeet.user_with)


@admin_router.message(CreateMeet.user_with)
async def get_user_who(message: types.Message, state: FSMContext) -> None:
    await state.update_data({"user_with": message.text})
    await message.answer(
        text="Сотрудник записан, введите описание ко встречи",
    )
    await state.set_state(CreateMeet.description)


@admin_router.message(CreateMeet.description)
async def get_user_who(message: types.Message, state: FSMContext) -> None:
    await state.update_data({"description": message.text})
    await message.answer(
        text="Отлично, назначьте дату\n\nФормат 2025-10-10 10:20:00",
    )
    await state.set_state(CreateMeet.date)


@admin_router.message(CreateMeet.date)
async def get_user_who(message: types.Message, state: FSMContext) -> None:
    await state.update_data({"date": message.text})
    await message.answer(text="Встреча назначена!")
    await state.clear()


# ========DELETE========
@admin_router.message(DeleteMeet.id_meet)
async def get_user_who(message: types.Message, state: FSMContext) -> None:
    await state.update_data({"id_meet": message.text})
    await message.answer(text="Отлично, идет обработка....")
    await state.clear()


# ========DELETE========
@admin_router.message(UpdateMeet.id_meet)
async def get_user_who(message: types.Message, state: FSMContext) -> None:
    await state.update_data({"id_meet": message.text})
    await message.answer(
        text="Отлично, этап изменения участника встречи",
        reply_markup=await InlineButtonFabric.build_buttons("skip")
    )
    await state.set_state(UpdateMeet.user_who)


@admin_router.message(UpdateMeet.user_who)
async def get_user_who(message: types.Message, state: FSMContext) -> None:
    await state.update_data({"user_who": message.text})
    await message.answer(
        text="Отлично, этап изменения второго участника встречи",
        reply_markup=await InlineButtonFabric.build_buttons("skip")
    )
    await state.set_state(UpdateMeet.user_with)


@admin_router.message(UpdateMeet.user_with)
async def get_user_who(message: types.Message, state: FSMContext) -> None:
    await state.update_data({"user_with": message.text})
    await message.answer(
        text="Отлично, этап изменения описания встречи",
        reply_markup=await InlineButtonFabric.build_buttons("skip")
    )
    await state.set_state(UpdateMeet.description)


@admin_router.message(UpdateMeet.description)
async def get_user_who(message: types.Message, state: FSMContext) -> None:
    await state.update_data({"description": message.text})
    await message.answer(
        text="Отлично, этап изменения даты встречи",
        reply_markup=await InlineButtonFabric.build_buttons("skip")
    )
    await state.set_state(UpdateMeet.date)


@admin_router.message(UpdateMeet.date)
async def get_user_who(message: types.Message, state: FSMContext) -> None:
    await state.update_data({"date": message.text})
    await message.answer(text="Отлично, идет обработка...")
    await state.clear()


# User
@admin_router.message(CreateUser.tg_id)
async def get_tgid_user(message: types.Message, state: FSMContext) -> None:
    await state.update_data({"tg_id": message.text})
    await message.answer(text='Отлично, теперь введите <b>номер телефона</b>, следующего формата <i>79823848383</i>')
    await state.set_state(CreateUser.user_phone)

@admin_router.message(CreateUser.user_phone)
async def get_phone_user(message: types.Message, state: FSMContext) -> None:
    await state.update_data({"user_phone": message.text})
    await message.answer(text='Отлично, теперь введите <b>должность</b> сотрудника')
    await state.set_state(CreateUser.post)

@admin_router.message(CreateUser.post)
async def get_post_user(message: types.Message, state: FSMContext) -> None:
    await state.update_data({"post": message.text})
    await message.answer(text='Отлично, теперь введите дату вступления в должность сотрудника')
    await state.set_state(CreateUser.date_start)

@admin_router.message(CreateUser.date_start)
async def get_date_user(message: types.Message, state: FSMContext) -> None:
    await state.update_data({"date_start": message.text})
    await message.answer(text='Идет обработка...')

    try:
        user_is_created = await UserModelRepository().create(
            new_model=UserModel(
                id_user_type=1,
                user_name="Инкогнито",
                user_phone=await state.get_value("user_phone"),
                post=await state.get_value("post"),
                tg_id=await state.get_value("tg_id"),
                date_start=datetime.datetime.strptime(await state.get_value("date_start"), "%Y-%m-%d")
            )
        )

        await state.clear()
        if user_is_created:
            await message.answer("Отлично, сотрудник был внесен в базу данных")
            return None

        raise Exception("Не удалось добавить пользователя")
    except Exception:
        await message.answer("Не удалось добавить сотрудника")