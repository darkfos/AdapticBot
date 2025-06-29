from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.database import DBWorker
from src.database.sqlite.repository.general_repository import GeneralRepository
from src.database.sqlite.models.memo_model import MeetModel
from src.database.sqlite.models.user_model import UserModel


class MeetModelRepository(GeneralRepository):
    def __init__(self):
        super().__init__(MeetModel)

    @classmethod
    async def get_all_by_user(cls, tg_id: int):
        session: AsyncSession = await DBWorker.get_session()
        try:
            data = select(MeetModel).join(UserModel, UserModel.id == MeetModel.id_who)

            if tg_id:
                data = data.where(UserModel.tg_id == tg_id)

            data = data.options(
                joinedload(MeetModel.user_who_data),
                joinedload(MeetModel.user_with_data),
            )

            result = await session.execute(data)
            return result.scalars().all()
        finally:
            await session.close()
