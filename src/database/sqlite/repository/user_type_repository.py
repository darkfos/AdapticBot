from sqlalchemy.ext.asyncio import AsyncSession

from src.database.sqlite.repository.general_repository import GeneralRepository
from src.database.sqlite.models.user_type_model import UserTypeModel


class UserTypeModelRepository(GeneralRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, UserTypeModel)