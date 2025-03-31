from aiogram.filters import BaseFilter
from aiogram.types import Message
from src.database.sqlite.repository.user_repository import UserModelRepository


class UserFilter(BaseFilter):

    async def __call__(self, message: Message) -> bool:
        if message.text == "/profile":
            is_auth = await UserModelRepository.iam_created(tg_id=message.from_user.id, phone_number="")
            if is_auth: return True
            await message.answer(text="Вы не числитесь в сотрудниках компании!")
            return is_auth
