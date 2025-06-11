from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.exceptions import TelegramRetryAfter
from aiogram.fsm.storage.memory import MemoryStorage


from src.settings import TelegramBotSettings
from src.core.routers import command_router
from src.core.routers import message_router
from src.core.service.admin.admin_main_service import admin_router
from src.core.service.user.user_main_service import user_profile_router
from src.core.configurations import (
    set_description_on_bot,
    set_my_short_description_on_bot,
    set_my_commands,
    set_chat_menu_buttons,
    set_bot_name,
)
from src.core.configurations import BotGeneralSettings as gs


class TelegramBot:

    def __init__(self) -> None:
        self.__bot: Bot = Bot(
            token=TelegramBotSettings().telegram_bot_token,
            default=DefaultBotProperties(parse_mode=gs.PARS_MODE.value),
        )
        self.storage = MemoryStorage()
        self.__dispatcher: Dispatcher = Dispatcher(
            storage=self.storage, fsm_strategy=gs.STRATEGY
        )

    async def include_dep(self) -> None:
        """
        Include other depedencies in bot
        :return:
        """

        self.__dispatcher.include_routers(
            command_router, user_profile_router, admin_router, message_router
        )

    async def set_configs(self) -> None:
        """
        Set configuration on bot
        :return:
        """

        try:
            await set_description_on_bot(self.__bot)
            await set_my_short_description_on_bot(self.__bot)
            await set_my_commands(self.__bot)
            await set_chat_menu_buttons(self.__bot)
            await set_bot_name(self.__bot)
        except TelegramRetryAfter:
            pass

    async def start_bot(self) -> None:
        """
        Start bot
        :return:
        """

        await self.include_dep()  # Include depedencies
        await self.set_configs()  # Set configurations
        await self.__bot.delete_webhook(
            drop_pending_updates=True
        )  # Delete old messages
        await self.__dispatcher.start_polling(self.__bot)

    @property
    async def get_bot(self) -> Bot:
        return self.__bot
