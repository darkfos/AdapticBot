from sqlalchemy.ext.asyncio import AsyncSession

from src.database.sqlite.repository.general_repository import GeneralRepository
from src.database.sqlite.models.user_model import UserModel


class UserModelRepository(GeneralRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, UserModel)