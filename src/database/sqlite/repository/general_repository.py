from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete, update
from typing import Union, Type

from src.database import DBWorker
from src.database.sqlite.models import user_model, user_type_model, memo_model


class GeneralRepository:

    def __init__(self,
                 model: Union[
                     Type[user_model.UserModel],
                     Type[user_type_model.UserTypeModel],
                     Type[memo_model.MeetModel]
                 ]):
        self.session: AsyncSession = None
        self.model = model

    async def get_one(self, id_: int):
        self.session = await DBWorker.get_session()
        stmt = select(self.model).where(self.model.id == id_)
        result = await self.session.execute(stmt)
        return result.one()

    async def get_all(self):
        self.session = await DBWorker.get_session()
        stmt = select(self.model)
        result = await self.session.execute(stmt)
        return result.all()

    async def create(self, new_model) -> bool:
        try:
            self.session = await DBWorker.get_session()
            stmt = insert(self.model).values(new_model.read_model())
            await self.session.execute(stmt)
            await self.session.commit()
            return True
        except Exception:
            return False

    async def delete(self, id_: int) -> bool:
        try:
            self.session = await DBWorker.get_session()
            stmt = delete(self.model).where(self.model.id == id_)
            await self.session.execute(stmt)
            await self.session.commit()
            return True
        except Exception:
            return False

    async def update(self, update_data_model) -> bool:
        try:
            self.session = await DBWorker.get_session()
            stmt = update(self.model).where(self.model.id == update_data_model.id).values(update_data_model.read())
            await self.session.execute(stmt)
            await self.session.commit()
            return True
        except Exception:
            return False
