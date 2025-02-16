"Запуск бота tinkoff_pulse_analysis"
import asyncio
import os
import logging
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

import bot_common


load_dotenv()

logging.basicConfig(level=logging.INFO)


async def main():
    """Запуск бота"""
    bot = Bot(token=os.environ['BOT_BM_TOKEN'])
    dp = Dispatcher()

    dp.include_routers(
        bot_common.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
