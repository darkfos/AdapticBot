from enum import Enum
from typing import Final


class CommandsTextsEnum(Enum):

    START_COMMAND_MESSAGE: Final[
        str
    ] = """
    <b>Привет!</b> Я адаптационный чат-бот который поможет тебе:\n
    
<b>1.</b> Получить актуальные сведения о компании 📌
<b>2.</b> Обуздать программу обучения 📈
<b>3.</b> Буду напоминать тебе о запланированных встречах 📆
<b>4.</b> Храню ссылки на регламенты, внутренние документы, чек-листы 📝
    """  # noqa

    HELP_COMMAND_MESSAGE: Final[str] = "Помощь"

    INFO_COMMAND_MESSAGE: Final[str] = "Информация"

    MEMO_COMMAND_MESSAGE: Final[str] = "Памятка"

    CLEAR_COMMAND_MESSAGE: Final[str] = "Состояние было успешно сброшено"
