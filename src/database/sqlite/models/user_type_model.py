from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String
from typing import List, Any


# Local
from src.database.sqlite.models.main_model import MainBase


class UserTypeModel(MainBase):

    name_type: Mapped[str] = mapped_column(type_=String(length=60))

    # Relations
    users: Mapped[List["UserModel"]] = relationship(
        "UserModel", back_populates="user_type", uselist=True
    )

    def __str__(self) -> str:
        return self.__name__.lower()

    def __repr__(self) -> str:
        return self.__name__.lower()

    def read_model(self) -> dict[str, Any]:
        return {k: v for k, v in self.__dict__.items()}
