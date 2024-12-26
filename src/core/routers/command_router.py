from aiogram import Router
from aiogram.filters import CommandStart, Command  # noqa
from aiogram.types import Message
from aiogram.enums.parse_mode import ParseMode


from src.enums import CommandsTextsEnum


command_router: Router = Router(name="commands")


@command_router.message(CommandStart())
async def start_command(message: Message) -> None:
    await message.answer(
        text=CommandsTextsEnum.START_COMMAND_MESSAGE.value,
        parse_mode=ParseMode.HTML,  # noqa
    )
