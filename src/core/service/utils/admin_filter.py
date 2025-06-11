from src.settings import TelegramBotSettings


async def is_admin(id_: int) -> bool:
    return int(id_) in TelegramBotSettings().admins_list
