from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String
from typing import List


# Local
from src.database.sqlite.models.main_model import MainBase


class UserTypeModel(MainBase):

    name_type: Mapped[str] = mapped_column(type_=String(length=60))

    # Relations
    users: Mapped[List["UserModel"]] = relationship(back_populates="UserModel.user_type", uselist=True)

    def __str__(self) -> str:
        return self.__name__.lower()

    def __repr__(self) -> str:
        return self.__name__.lower()
