import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, DateTime, ForeignKey, Integer
from typing import Any

# Local
from src.database.sqlite.models.main_model import MainBase


class MeetModel(MainBase):

    # Кому запланирована встреча
    id_who: Mapped[int] = mapped_column(ForeignKey("usermodel.id"), type_=Integer)

    # С кем запланирована встреча
    id_with: Mapped[int] = mapped_column(ForeignKey("usermodel.id"), type_=Integer)

    # Пояснение к встрече
    description: Mapped[str] = mapped_column(type_=Text, nullable=True, index=False, unique=False)

    # Дата встречи
    date_meeting: Mapped[datetime.datetime] = mapped_column(type_=DateTime, nullable=True, index=False, unique=False)

    # Формат уведомления
    time_format: Mapped[int] = mapped_column(type_=Integer, nullable=True)

    user_who_data: Mapped["UserModel"] = relationship("UserModel", foreign_keys=[id_who], back_populates="meets_who_user", uselist=False)
    user_with_data: Mapped["UserModel"] = relationship("UserModel", foreign_keys=[id_with], back_populates="meets_with_user", uselist=False)

    def __str__(self):
        return str({
            k: v
            for k,v in self.__dict__.items()
        })

    def __repr__(self):
        return self.__str__()

    async def read_model(self) -> dict[str, Any]:
        return {
            k: v
            for k,v in self.__dict__.items()
            if not k.startswith("_")
        }