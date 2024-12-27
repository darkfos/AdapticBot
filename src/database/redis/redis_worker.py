from redis.asyncio import Redis
from typing import Any


from src.settings import DatabaseSettings
from src.core.configurations import BotGeneralSettings


class RedisWorker:

    __redis: Redis = Redis(host=DatabaseSettings().redis_host, port=int(DatabaseSettings().redis_port))

    @classmethod
    async def set_value(cls, key, value) -> None:
        await cls.__redis.set(name=key, value=value, ex=DatabaseSettings().redis_time_life)

    @classmethod
    async def get_value(cls, key) -> Any:
        return await cls.__redis.get(name=key)


    @classmethod
    async def set_key_tg(cls, key) -> bool:
        user_data = await cls.get_value(key=key)
        if user_data is not None:
            return await cls.set_message_tg_user(key=key)
        await cls.__redis.set(name=key, value=0, ex=DatabaseSettings().redis_time_life)


    @classmethod
    async def set_message_tg_user(cls, key) -> bool:
        user_data = await cls.get_value(key=key)
        user_data = int(user_data.decode("utf-8"))

        if user_data > BotGeneralSettings.LIMIT_MESSAGE:
            return False
        await cls.__redis.set(name=key, value=user_data+1, ex=DatabaseSettings().redis_time_life)
        return True