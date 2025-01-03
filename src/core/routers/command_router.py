from aiogram import Router
from aiogram.filters import CommandStart, Command  # noqa
from aiogram.methods import EditMessageText, AnswerCallbackQuery
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F
from typing import Union


from src.enums import CommandsTextsEnum

### BUTTONS ###
from src.core.buttons.inline import InlineButtonFabric


command_router: Router = Router(name="commands")


@command_router.message(CommandStart())
async def start_command(message: Message) -> None:
    await message.answer(
        text=CommandsTextsEnum.START_COMMAND_MESSAGE.value,
        reply_markup=await InlineButtonFabric.build_buttons("general")
    )


@command_router.message(Command("help"))
async def help_command(message: Message) -> None:
    await message.answer(
        text=CommandsTextsEnum.HELP_COMMAND_MESSAGE.value,
    )


@command_router.message(Command("info"))
async def info_command(message: Message) -> None:
    await message.answer(
        text=CommandsTextsEnum.INFO_COMMAND_MESSAGE.value,
    )


@command_router.message(Command("memo"))
async def memo_command(message: Message) -> None:
    await message.answer(
        text=CommandsTextsEnum.MEMO_COMMAND_MESSAGE.value,
    )

@command_router.message(Command('clear'))
async def clear_command(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        text=CommandsTextsEnum.CLEAR_COMMAND_MESSAGE.value,
    )


@command_router.callback_query(F.data.startswith("/"))
async def query_to_commands(message: CallbackQuery) -> Union[EditMessageText, AnswerCallbackQuery]:
    match message.data:
        case "/help":
            return await message.message.edit_text(
                text=CommandsTextsEnum.HELP_COMMAND_MESSAGE.value,
                reply_markup=await InlineButtonFabric.build_buttons("back")
            )
        case "/memo":
            return await message.message.edit_text(
                text=CommandsTextsEnum.MEMO_COMMAND_MESSAGE.value,
                reply_markup=await InlineButtonFabric.build_buttons("back")
            )
        case "/info":
            return await message.message.edit_text(
                text=CommandsTextsEnum.INFO_COMMAND_MESSAGE.value,
                reply_markup=await InlineButtonFabric.build_buttons("back")
            )
        case "/back":
            return await message.message.edit_text(
                text=CommandsTextsEnum.START_COMMAND_MESSAGE.value,
                reply_markup=await InlineButtonFabric.build_buttons("general")
            )
        case "_":
            return await message.answer(text="Опция не найдена..")
