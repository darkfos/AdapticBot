from pydantic_settings import BaseSettings, SettingsConfigDict


class TelegramBotSettings(BaseSettings):
    telegram_bot_token: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
