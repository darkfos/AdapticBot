from enum import Enum
from typing import Final


class ErrosTextEnum(Enum):
    SPAM_ERROR: Final[str] = "Вы превысили лимит сообщений! Пожалуйста подождите..."
    