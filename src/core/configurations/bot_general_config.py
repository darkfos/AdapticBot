from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.strategy import FSMStrategy
from typing import Final


class BotGeneralSettings:

    PARS_MODE: Final[ParseMode.HTML] = ParseMode.HTML
    STRATEGY: Final[FSMStrategy.CHAT] = FSMStrategy.CHAT
    LIMIT_MESSAGE: Final[int] = 3

    def __setattr__(self, key, value):
        if key in self.__dict__:
            return
        else:
            self.__dict__[key] = value
