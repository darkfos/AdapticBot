from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from src.settings.tg_bot_settings import TelegramBotSettings


class AdminFilter(BaseFilter):

    async def __call__(self, message: Message):
        if message.from_user.id in TelegramBotSettings().admins_list:
            return True
        return False