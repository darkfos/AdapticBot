from datetime import datetime
import asyncio
from aiogram import Bot

from src.database.sqlite.repository.meet_repository import MeetModelRepository
from src.database.sqlite.repository.user_repository import UserModelRepository
from src.database.sqlite.models.memo_model import MeetModel
from src.settings import TelegramBotSettings


bot: Bot = Bot(TelegramBotSettings().telegram_bot_token)


async def check_memo() -> None:
    while True:
        meets: list[MeetModel] = await MeetModelRepository().get_all()
        for meet in meets:
            await send_notification(
                meet.id_with,
                meet.id_who,
                meet.id,
                meet.time_format,
                meet.date_meeting,
                meet.description
            )
        await asyncio.sleep(86400)


async def send_notification(id_who: int, id_with: int, id_meet: int, notification_format: int, time: datetime, description: str) -> None:
    """
    Отправка уведомления
    """

    try:
        date_now = datetime.now()

        if date_now > time:
            return await MeetModelRepository().delete(id_=id_meet)


        if notification_format == 1:  # Каждый день
            if date_now.date() == time.date():
                await _send_notification(id_who, id_with, time, description)
        elif notification_format == 3:  # Каждые 3 дня
            if (date_now - time).days % 3 == 0:
                await _send_notification(id_who, id_with, time, description)
        elif notification_format == 7:  # Каждую неделю
            if (date_now - time).days % 7 == 0:
                await _send_notification(id_who, id_with, time, description)
        elif notification_format == 30:  # Каждый месяц
            if date_now.day == time.day:
                await _send_notification(id_who, id_with, time, description)
        else:
            await _send_notification(id_who, id_with, time, description)

    except Exception:
        pass

async def _send_notification(id_who: int, id_with: int, time: datetime, description: str) -> None:
    """
    Функция для отправки уведомления
    """
    user_who_data = (await UserModelRepository().get_one(id_who))[0]
    user_with_data = (await UserModelRepository().get_one(id_with))[0]

    await bot.send_message(
        chat_id=user_who_data.tg_id,
        text=f"📌 Напоминание о встрече\n\n"
             f"⏰ <b>Время:</b> {time}\n\n"
             f"🧓 <b>С кем:</b> {user_with_data.user_name}\n\n"
             f"📑 <b>Пояснение ко встрече:</b> {description}"
    )


async def send_notification_from_admin_panel() -> None:
    """
    Отправка уведомления
    """

    meets: list[MeetModel] = await MeetModelRepository().get_all()

    for meet in meets:

        user_who_data = (await UserModelRepository().get_one(meet.id_who))
        user_with_data = (await UserModelRepository().get_one(meet.id_with))
        bot: Bot = Bot(TelegramBotSettings().telegram_bot_token)

        if (user_who_data and user_with_data):
            await bot.send_message(
                chat_id=user_who_data[0].tg_id,
                text=f"📌 Напоминание о встрече\n\n"
                     f"⏰ <b>Время:</b> {meet.date_meeting}\n\n"
                     f"🧓 <b>С кем:</b> {user_with_data[0].user_name}\n\n"
                     f"📑 <b>Пояснение ко встрече:</b> {meet.description}"
            )