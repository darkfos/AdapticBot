import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.types import String, BigInteger, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Any

# Local
from src.database.sqlite.models.main_model import MainBase


class UserModel(MainBase):

    id_user_type: Mapped[int] = mapped_column(ForeignKey("usertypemodel.id"))
    user_phone: Mapped[str] = mapped_column(type_=String(length=25), nullable=True, index=True)
    post: Mapped[str] = mapped_column(type_=String(200), nullable=True, index=True)
    tg_id: Mapped[int] = mapped_column(type_=BigInteger, nullable=True, index=True)
    date_start: Mapped[datetime.date] = mapped_column(type_=Date, nullable=True, index=False, default=datetime.date.today())


    # Relations
    user_type: Mapped["UserTypeModel"] = relationship("UserTypeModel", back_populates="users", uselist=False)

    def __str__(self) -> str:
        return str({
            k: v
            for k, v in self.__dict__.items()
        })

    def __repr__(self) -> str:
        return self.__str__()

    async def read_model(self) -> dict[str, Any]:
        return {
            k: v
            for k,v in self.__dict__.items()
            if k not in ("_sa_instance_state", "id")
        }