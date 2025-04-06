from sqlalchemy.ext.asyncio import AsyncSession

from src.database.sqlite.repository.general_repository import GeneralRepository
from src.database.sqlite.models.user_model import UserModel
from src.database.sqlite.db_worker import DBWorker
from sqlalchemy import select


class UserModelRepository(GeneralRepository):
    def __init__(self):
        super().__init__(UserModel)

    @classmethod
    async def iam_created(cls, tg_id: int = None, phone_number: str = None):
        session: AsyncSession = await DBWorker.get_session()

        if tg_id:
            user_is_created = await session.execute(select(UserModel).where(UserModel.tg_id == tg_id))
        else:
            user_is_created = await session.execute(select(UserModel).where(UserModel.user_phone == phone_number))

        user_data = user_is_created.one_or_none()
        await session.close()
        return user_data

    @classmethod
    async def find_by_phone(cls, phone_number: str):
        session: AsyncSession = await DBWorker.get_session()
        user_is_created = await session.execute(select(UserModel).where(UserModel.user_phone == phone_number))
        user_data = user_is_created.one_or_none()
        await session.close()
        return user_data
