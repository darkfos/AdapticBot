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
    
📌 <b>Получить актуальные сведения о компании</b>
📈 <b>Обуздать программу обучения</b>
📆 <b>Буду напоминать тебе о запланированных встречах</b>
📝 <b>Храню ссылки на регламенты, внутренние документы, чек-листы</b>
    """  # noqa

    HELP_COMMAND_MESSAGE: Final[str] = """
<b>Пункт помощи.</b>\n\n

🤖 <b>Команды</b>\n\n
📍 <i>/start</i> - Стартовая команда\n
📍 <i>/help</i> - Пункт помощи, руководство по использованию бота\n
📍 <i>/info</i> - Матрица коммуникаций\n
📍 <i>/memo</i> - Памятка сотруднику\n
📍 <i>/clear</i> - Очистка состояния, на случай каких-либо непредвиденных ошибок, очищает состояние\n
📍 <i>/profile</i> - Личный профиль пользователя
📍 <i>/admin</i> - Панель администратора
📍 <i>/success</i> - Подтверждение аккаунта

\n\n
🤖 <b>Руководство пользователя</b>\n\n
Пользователь может получать уведомления, просматривать информацию по матрице коммуникаций, памятке,
пользоваться личным кабинетам и в режиме реального времени просматривать какие у него запланированы встречи.

\n\n
🤖 <b>Руководство администратора</>\n\n
Администратор имеет полные права по использованию функционала данного бота.\n
📍 <i>/admin</i> - Вход в админ панель, имеются следующие возможности:\n
📍. Добавление сотрудника
📍. Посмотреть список всех сотрудников
📍. Создать встречу
📍. Посмотреть какие есть на данные момент встречи
📍. Удалить встречу
📍. Изменить данные о встрече\n

\n\n
🤖 <b>Авторизация новых сотрудников</b>\n\n
После того как был добавлен новый сотрудник ему необходимо подвердить свой аккаунт, а именно привязать свой номер телефона,
сделать это можно с помощью команды /success, в нижней панели появится кнопка для отправки контакта, данную операцию
необходимо сделать <b>всем</b> сотрудникам которые были недавно добавлены в систему.
    """

    INFO_COMMAND_MESSAGE: Final[str] = emojize("Добро пожаловать в матрицу коммуникаций!\n\n<b>Ссылки на наши ресурсы:</b>\n\n" \
                                        f":star: Instagram - {InfoData.instagram_url}\n\n" \
                                        f":star: Vk - {InfoData.vk_url}\n\n" \
                                        f":star: Cloud - {InfoData.cloud}\n\n")

    MEMO_COMMAND_MESSAGE: Final[str] = "<b>Памятка новому сотруднику</b>"

    CLEAR_COMMAND_MESSAGE: Final[str] = "Состояние было успешно сброшено"
