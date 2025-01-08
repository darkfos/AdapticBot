from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
    AsyncSession
)


# Local
from src.database.sqlite.models.main_model import MainBase
from src.settings import DatabaseSettings


class DBWorker:
    __db: AsyncEngine = create_async_engine(
        url=DatabaseSettings().main_db_url,
    )

    __session_maker = async_sessionmaker(
        bind=__db,
        class_=AsyncSession
    )

    @classmethod
    async def get_session(cls) -> AsyncSession:
        async with cls.__session_maker.begin() as ls:
            return ls

    @classmethod
    async def create_models(cls) -> None:
        async with cls.__db.begin() as ls:
            await ls.run_sync(MainBase.metadata.create_all)

    @classmethod
    async def delete_models(cls) -> None:
        async with cls.__db.begin() as ls:
            await ls.run_sync(MainBase.metadata.drop_all)
