from sqlalchemy import ForeignKey
from sqlalchemy.types import String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Any

# Local
from src.database.sqlite.models.main_model import MainBase


class UserModel(MainBase):

    id_user_type: Mapped[int] = mapped_column(ForeignKey("usertypemodel.id"))
    user_name: Mapped[str] = mapped_column(type_=String(length=255), nullable=False, index=False)
    tg_id: Mapped[int] = mapped_column(type_=BigInteger, nullable=False, index=True)


    # Relations
    user_type: Mapped["UserTypeModel"] = relationship(back_populates="UserTypeModel.users", uselist=False)

    def __str__(self) -> str:
        return self.__name__.capitalize()

    def __repr__(self) -> str:
        return self.__str__()

    def read_model(self) -> dict[str, Any]:
        return {
            k: v
            for k,v in self.__dict__.items()
        }