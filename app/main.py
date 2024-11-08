# main.py
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from core.config import settings
from core.logger import setup_logging
from handlers import register_all_handlers
from infrastructure.database.orm import AsyncSessionLocal
from middlewares import (
    DbSessionMiddleware,
    S3Middleware,
    SubscriptionMiddleware,
)
from redis.asyncio import Redis
from scheduler.broadcast import start_scheduler


async def main() -> None:
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()

    # Добавление middleware
    dp.update.middleware(DbSessionMiddleware())
    dp.update.middleware(SubscriptionMiddleware(redis))
    dp.update.middleware(S3Middleware())

    # Регистрация обработчиков
    register_all_handlers(dp)

    # Запуск планировщика
    start_scheduler(bot, session_factory=AsyncSessionLocal)

    # Начало polling
    await dp.start_polling(bot)


if __name__ == "__main__":
    setup_logging()
    logging.info("Запуск бота")
    redis = Redis.from_url(
        settings.REDIS_URL, encoding="utf-8", decode_responses=True
    )
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен")
