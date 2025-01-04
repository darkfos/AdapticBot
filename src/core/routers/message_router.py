from aiogram.types import Message
from aiogram import Router


message_router: Router = Router(name="message")


@message_router.message()
async def other_messages(message: Message) -> None:
    """
    Router for check other messages from user
    :param message:
    :return:
    """

    await message.answer(
        text="Не понимаю вашу команду. \n<b>Введите</b> /help для получения помощи.."  # noqa
    )
