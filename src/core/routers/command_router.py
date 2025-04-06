from aiogram import Router, Bot
from aiogram.filters import CommandStart, Command  # noqa
from aiogram.methods import EditMessageText, AnswerCallbackQuery
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, FSInputFile, InputFile
from aiogram.fsm.context import FSMContext
from aiogram import F
from typing import Union

from src.core.buttons.reply import ReplyButtonFabric
from src.enums.texts import GeneralCommands
from src.enums import CommandsTextsEnum
from src.settings.tg_bot_settings import TelegramBotSettings
from src.core.filters.admin_filter import AdminFilter
from src.core.filters.user import UserFilter
from src.database.sqlite.repository.user_repository import UserModelRepository
from src.database.sqlite.models.user_model import UserModel

# BUTTONS
from src.core.buttons.inline import InlineButtonFabric

bot: Bot = Bot(token=TelegramBotSettings().telegram_bot_token)
command_router: Router = Router(name="commands")


@command_router.message(CommandStart())
async def start_command(message: Message) -> None:
    """
    Start command
    :param message:
    :return:
    """

    start_message = await message.answer(
        text=CommandsTextsEnum.START_COMMAND_MESSAGE.value,
        reply_markup=await InlineButtonFabric.build_buttons("general_tests"),
    )

    await message.chat.pin_message(start_message.message_id)


@command_router.message(Command(GeneralCommands.HELP.value))
async def help_command(message: Message) -> None:
    """
    Help command
    :param message:
    :return:
    """

    await message.answer(
        text=CommandsTextsEnum.HELP_COMMAND_MESSAGE.value,
        reply_markup=ReplyKeyboardRemove(),
    )


@command_router.message(Command(GeneralCommands.INFO.value))
async def info_command(message: Message) -> None:
    """
    Info command
    :param message:
    :return:
    """

    await message.answer_document(
        document=FSInputFile(path="src/static/img/commutication_matrics.pdf"),
        caption=CommandsTextsEnum.INFO_COMMAND_MESSAGE.value,
        reply_markup=ReplyKeyboardRemove()
    )


@command_router.message(Command(GeneralCommands.MEMO.value))
async def memo_command(message: Message) -> None:
    """
    Memo command
    :param message:
    :return:
    """

    await message.answer(
        text=CommandsTextsEnum.MEMO_COMMAND_MESSAGE.value,
        reply_markup=ReplyKeyboardRemove(),
    )


@command_router.message(Command(GeneralCommands.CLEAR.value))
async def clear_command(message: Message, state: FSMContext) -> None:
    """
    Clear command

    :param message:
    :param state:
    :return:
    """

    await state.clear()
    await message.answer(
        text=CommandsTextsEnum.CLEAR_COMMAND_MESSAGE.value,
        reply_markup=await ReplyButtonFabric.build_buttons("general_tests"),
    )


@command_router.message(
    AdminFilter(),
    Command(GeneralCommands.ADMIN.value)
)
async def admin_command(message: Message) -> None:
    """
    Admin command

    :param message:
    :return:
    """

    if message.from_user.id in TelegramBotSettings().admins_list:
        from src.enums.texts.admin_panel import admin_panel_text
        await message.answer(
            text=await admin_panel_text(message.from_user.first_name),
            reply_markup=await InlineButtonFabric.build_buttons("admin")
        )

    else:
        await message.answer(
            text="Доступ к админ панели запрещен."
        )


@command_router.message(Command(GeneralCommands.SUCCESS.value))
async def success_persona(message: Message) -> None:
    await message.answer(text="Для активации аккаунта, нажмите на кнопку в нижней панели.", reply_markup=await ReplyButtonFabric.build_buttons("contact"))


@command_router.message(UserFilter(), Command(GeneralCommands.PROFILE.value))
async def profile_command(message: Message) -> None:

    user_data: UserModel = await UserModelRepository().iam_created(tg_id=message.from_user.id)
    user_data = user_data[0]

    user_photo = await bot.get_user_profile_photos(user_id=user_data.tg_id)

    await message.answer_photo(
        photo=user_photo.photos[0][0].file_id,
        caption=(f"\n<b>Мой профиль</b> \n\n" +
              f"<b>Имя:</b> {user_data.user_name}\n\n"
              f"<b>Номер телефона:</b> {user_data.user_phone if user_data.user_phone else 'Отсутствует'}\n\n"
              f"<b>Должность:</b> {user_data.post if user_data.post else 'Отсутствует'}\n\n"
              f"<b>Дата вступления:</b> {user_data.date_start}"),
        reply_markup=await InlineButtonFabric.build_buttons("profile")
    )


@command_router.callback_query(F.data.startswith("/"))
async def query_to_commands(
    message: CallbackQuery,
) -> Union[EditMessageText, AnswerCallbackQuery]:
    """
    Callback query for check btn event (USABILITY)
    :param message:
    :return:
    """

    match message.data:
        case "/start":
            return await message.message.edit_text(
                text=CommandsTextsEnum.HELP_COMMAND_MESSAGE.value,
                reply_markup=await InlineButtonFabric.build_buttons("back"),
            )
        case "/memo":
            return await message.message.edit_text(
                text=CommandsTextsEnum.MEMO_COMMAND_MESSAGE.value,
                reply_markup=await InlineButtonFabric.build_buttons("back"),
            )
        case "/info":
            return await message.message.edit_text(
                text=CommandsTextsEnum.INFO_COMMAND_MESSAGE.value,
                reply_markup=await InlineButtonFabric.build_buttons("back"),
            )
        case "/back":
            return await message.message.edit_text(
                text=CommandsTextsEnum.START_COMMAND_MESSAGE.value,
                reply_markup=await InlineButtonFabric.build_buttons(
                    "general_tests"
                ),  # noqa
            )
        case "_":
            return await message.answer(text="Опция не найдена..")