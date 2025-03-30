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
        "/info - Матрица коммуникаций",
        "/memo - Памятка сотрудника",
        "/help -  Помощь",
        "/clear - Очистка",
        "/admin - Админ панель"
    ]

    BOT_NAME: Final[str] = "Адаптик"
