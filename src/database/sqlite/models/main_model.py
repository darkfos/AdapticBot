from sqlalchemy import Integer
from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
    Mapped,
    mapped_column
)


class MainBase(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, type_=Integer, autoincrement=True)

    @classmethod
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
