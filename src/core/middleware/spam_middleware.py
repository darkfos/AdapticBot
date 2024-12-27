from typing import Callable, Dict, Any, Awaitable
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import TelegramObject
from src.enums import ErrosTextEnum


from src.database import RedisWorker


class SpamMiddleware(BaseMiddleware):

    def __init__(self, seconds: int = 1.5) -> None:
        self.seconds = seconds

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        """
        Logging middleware
        :param hander:
        :param event:
        :param data:
        :return:
        """

        user_id: int = data.get("event_context").chat.id
        result = await RedisWorker.set_key_tg(key=user_id)
        if result is False:
            await event.answer(text=ErrosTextEnum.SPAM_ERROR.value)
            return
        return await handler(event, data)
