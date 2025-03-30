from sqlalchemy.ext.asyncio import AsyncSession

from src.database.sqlite.repository.general_repository import GeneralRepository
from src.database.sqlite.models.memo_model import MeetModel


class MeetModelRepository(GeneralRepository):
    def __init__(self):
        super().__init__(MeetModel)