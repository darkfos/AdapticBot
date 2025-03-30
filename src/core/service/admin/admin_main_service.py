from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from src.core.filters.admin_filter import AdminFilter
from src.database.sqlite.repository.meet_repository import MeetModelRepository
from src.core.service.admin.states.general_states import CreateMeet, DeleteMeet, UpdateMeet
from src.core.buttons.inline import InlineButtonFabric

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
