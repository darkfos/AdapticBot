import asyncio

# Local
from src import TelegramBot
from src.notifications.notifications_service import check_memo


async def main():
    bot = TelegramBot()

    await asyncio.gather(bot.start_bot(), check_memo())


if __name__ == "__main__":
    asyncio.run(main())
