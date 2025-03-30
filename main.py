import asyncio

# Local
from src import TelegramBot


if __name__ == "__main__":
    bot = TelegramBot()
    asyncio.run(bot.start_bot())