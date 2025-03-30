import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, Text, DateTime
from typing import Any


# Local
from src.database.sqlite.models.main_model import MainBase


class MeetModel(MainBase):

    # Кому запланирована встреча
    id_who: Mapped[int] = mapped_column(type_=BigInteger, index=True, unique=False)

    # С кем запланирована встреча
    id_with: Mapped[int] = mapped_column(type_=BigInteger, index=True, unique=False, nullable=True)

    # Пояснение к встрече
    description: Mapped[str] = mapped_column(type_=Text, nullable=True, index=False, unique=False)

    # Дата встречи
    date_meeting: Mapped[datetime.datetime] = mapped_column(type_=DateTime, nullable=True, index=False, unique=False)

    def __str__(self):
        return str({
            k: v
            for k,v in self.__dict__.items()
        })

    def __repr__(self):
        return self.__str__()

    def read_model(self) -> dict[str, Any]:
        return {
            k: v
            for k,v in self.__dict__.items()
        }