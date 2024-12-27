from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):

    # Redis
    redis_host: str
    redis_port: str
    redis_time_life: int

    # Sqlite

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
