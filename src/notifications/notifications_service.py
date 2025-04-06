from datetime import datetime
import asyncio
from aiogram import Bot

from src.database.sqlite.repository.meet_repository import MeetModelRepository
from src.database.sqlite.repository.user_repository import UserModelRepository
from src.database.sqlite.models.memo_model import MeetModel
from src.settings import TelegramBotSettings


async def check_memo() -> None:
    while True:
        meets: list[MeetModel] = await MeetModelRepository().get_all()
        for meet in meets:
            await send_notification(meet.id_with, meet.id_who, meet.id, meet.date_meeting, meet.description)
        await asyncio.sleep(86400)


async def send_notification(id_who: int, id_with: int, id_meet: int, time: datetime, description: str) -> None:
    """
    Отправка уведомления
    """

    try:

        date_now = datetime.now()

        if date_now > time:
            await MeetModelRepository().delete(id_=id_meet)

        else:
            user_who_data = (await UserModelRepository().get_one(id_who))[0]
            user_with_data = (await UserModelRepository().get_one(id_with))[0]
            bot: Bot = Bot(TelegramBotSettings().telegram_bot_token)

            await bot.send_message(
                chat_id=user_who_data.tg_id,
                text=f"Напоминание о встрече\n\n"
                     f"Время: {time}\n\n"
                     f"С кем: {user_with_data.user_name}\n\n"
                     f"Пояснение ко встрече: {description}"
            )

    except Exception:
        pass
