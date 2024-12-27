from aiogram.enums.parse_mode import ParseMode
from typing import Final


class BotGeneralSettings:
    PARS_MODE: Final[ParseMode.HTML] = ParseMode.HTML

    def __setattr__(self, key, value):
        if key in self.__dict__:
            return
        else:
            self.__dict__[key] = value