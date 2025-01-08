import asyncio


from src import TelegramBot
from src.database import DBWorker



if __name__ == "__main__":
    bot = TelegramBot()
    asyncio.run(bot.start_bot())