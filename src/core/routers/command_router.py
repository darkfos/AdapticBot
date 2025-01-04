from aiogram import Router
from aiogram.filters import CommandStart, Command  # noqa
from aiogram.methods import EditMessageText, AnswerCallbackQuery
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram import F
from typing import Union

from src.core.buttons.reply import ReplyButtonFabric
from src.enums import CommandsTextsEnum

# BUTTONS
from src.core.buttons.inline import InlineButtonFabric


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


@command_router.message(Command("help"))
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


@command_router.message(Command("info"))
async def info_command(message: Message) -> None:
    """
    Info command
    :param message:
    :return:
    """

    await message.answer(
        text=CommandsTextsEnum.INFO_COMMAND_MESSAGE.value,
        reply_markup=ReplyKeyboardRemove(),
    )


@command_router.message(Command("memo"))
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


@command_router.message(Command("clear"))
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
        case "/help":
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
