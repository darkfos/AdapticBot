from aiogram import Router
from aiogram.filters import CommandStart, Command  # noqa
from aiogram.types import Message
from aiogram.fsm.context import FSMContext


from src.enums import CommandsTextsEnum
from src.core.configurations import BotGeneralSettings as gs


command_router: Router = Router(name="commands")


@command_router.message(CommandStart())
async def start_command(message: Message) -> None:
    await message.answer(
        text=CommandsTextsEnum.START_COMMAND_MESSAGE.value,
        parse_mode=gs.PARS_MODE.value,  # noqa
    )


@command_router.message(Command("help"))
async def help_command(message: Message) -> None:
    await message.answer(
        text=CommandsTextsEnum.HELP_COMMAND_MESSAGE.value,
        parse_mode=gs.PARS_MODE.value
    )


@command_router.message(Command("info"))
async def info_command(message: Message) -> None:
    await message.answer(
        text=CommandsTextsEnum.INFO_COMMAND_MESSAGE.value,
        parse_mode=gs.PARS_MODE.value
    )


@command_router.message(Command("memo"))
async def memo_command(message: Message) -> None:
    await message.answer(
        text=CommandsTextsEnum.MEMO_COMMAND_MESSAGE.value,
        parse_mode=gs.PARS_MODE.value
    )


@command_router.message(Command("clear"))
async def clear_command(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        text=CommandsTextsEnum.CLEAR_COMMAND_MESSAGE.value,
        parse_mode=gs.PARS_MODE.value
    )
