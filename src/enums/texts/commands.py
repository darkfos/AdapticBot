from enum import Enum
from typing import Final
from emoji import emojize

class GeneralCommands(Enum):

    START: str = "start"
    HELP: str = "help"
    INFO: str = "info"
    MEMO: str = "memo"
    CLEAR: str = "clear"
    ADMIN: str = "admin"
    PROFILE: str = "profile"
    SUCCESS: str = "success"


class InfoData:
    instagram_url: str = "https://www.instagram.com/expert_klinika/"
    vk_url: str = "https://vk.com/mdcexpert"
    cloud: str = "https://cloud.mail.ru/public/VieN/4t8zyPG6M"


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

    INFO_COMMAND_MESSAGE: Final[str] = emojize("Добро пожаловать в матрицу коммуникаций!\n\n<b>Ссылки на наши ресурсы:</b>\n\n" \
                                        f":star: Instagram - {InfoData.instagram_url}\n\n" \
                                        f":star: Vk - {InfoData.vk_url}\n\n" \
                                        f":star: Cloud - {InfoData.cloud}\n\n")

    MEMO_COMMAND_MESSAGE: Final[str] = "Памятка"

    CLEAR_COMMAND_MESSAGE: Final[str] = "Состояние было успешно сброшено"
