import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import TELEGRAM_BOT_TOKEN
from handlers import start, token_check, wallet_check


async def main():
    logging.basicConfig(level=logging.INFO)

    if not TELEGRAM_BOT_TOKEN:
        raise RuntimeError(
            "TELEGRAM_BOT_TOKEN не встановлено. Створіть файл .env на основі .env.example "
            "і вкажіть там токен, отриманий від @BotFather."
        )

    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(token_check.router)
    dp.include_router(wallet_check.router)

    logging.info("Бот запущено, очікую повідомлення...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
