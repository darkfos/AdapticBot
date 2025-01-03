from enum import Enum
from typing import Final, List


class ConfigurationTextEnum(Enum):
    BOT_DESC: Final[str] = (
        "Я адаптационный бот! Который поможет тебе освоиться в компании.."
    )
    BOT_SHORT_DESC: Final[str] = (
        "Я адаптационный бот! Который поможет тебе освоиться в компании.."
    )

    COMMANDS_LIST: List[str] = [
        "/start - Запуск бота",
        "/info - Информация",
        "/memo - Памятка сотрудника",
        "/help -  Помощь",
        "/clear - Очистка",
    ]

    BOT_NAME: Final[str] = "Адаптик"
