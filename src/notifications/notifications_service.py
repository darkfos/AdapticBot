from datetime import datetime, timedelta
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
                meet
            )
        await asyncio.sleep(86400)


async def send_notification(
        meet: MeetModel
) -> None:
    """
    Отправка уведомления
    """

    try:
        date_now = datetime.now()

        if date_now > meet.date_meeting:
            return await MeetModelRepository().delete(id_=meet.id)

        print(date_now, meet)
        if not meet.date_last_meeting:
            await _send_notification(meet)
            return


        if meet.time_format == 1:  # Каждый день
            if date_now >= meet.date_last_meeting + timedelta(days=1):
                await _send_notification(meet)
        elif meet.time_format == 3:  # Каждые 3 дня
            if date_now >= meet.date_last_meeting + timedelta(days=3):
                await _send_notification(meet)
        elif meet.time_format >= 7:  # Каждую неделю
            if date_now >= meet.date_last_meeting + timedelta(days=7):
                await _send_notification(meet)
        elif meet.time_format >= 30:  # Каждый месяц
            if date_now >= meet.date_last_meeting + timedelta(days=30):
                await _send_notification(meet)

    except Exception as e:
        pass

async def _send_notification(
    meet: MeetModel
) -> None:
    """
    Функция для отправки уведомления
    """

    user_who_data = (await UserModelRepository().get_one(meet.id_who))[0]
    user_with_data = (await UserModelRepository().get_one(meet.id_with))[0]

    meet.date_last_meeting = datetime.now()
    await MeetModelRepository().update(meet)

    await bot.send_message(
        chat_id=user_who_data.tg_id,
        text=f"📌 Напоминание о встрече\n\n"
             f"⏰ Время: {meet.date_meeting}\n\n"
             f"🧓 С кем: {user_with_data.user_name}\n\n"
             f"📑 Пояснение ко встрече: {meet.description}"
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
                     f"⏰ Время: {meet.date_meeting}\n\n"
                     f"🧓 С кем: {user_with_data[0].user_name}\n\n"
                     f"📑 Пояснение ко встрече: {meet.description}"
            )