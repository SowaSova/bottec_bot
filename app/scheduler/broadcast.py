# scheduler/broadcast.py

import asyncio
import logging

from aiogram import exceptions
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from services.broadcast import BroadcastMessageService
from services.users import UserService

logger = logging.getLogger(__name__)
scheduler = AsyncIOScheduler()


async def send_broadcast_messages(bot, session_factory):
    logger.info("Начало отправки рассылок...")
    try:
        async with session_factory() as session:
            message_service = BroadcastMessageService(session)
            user_service = UserService(session)
            messages = await message_service.get_messages()
            users = await user_service.get_users()

            for message in messages:
                if not users:
                    logger.info("Нет пользователей для рассылки.")
                    break

                tasks = []
                for user in users:
                    tasks.append(send_message(bot, user, message.message_text))

                results = await asyncio.gather(*tasks, return_exceptions=True)

                for result, user in zip(results, users):
                    if isinstance(result, Exception):
                        if isinstance(result, exceptions.BotBlocked):
                            logger.warning(
                                f"Бот заблокирован пользователем {user.telegram_id}"
                            )
                        else:
                            logger.error(
                                f"Ошибка при отправке пользователю {user.telegram_id}: {result}"
                            )
                    else:
                        logger.info(
                            f"Сообщение отправлено пользователю {user.telegram_id}"
                        )

                await message_service.mark_as_sent(message)
                logger.info(
                    f"Сообщение {message.id} отмечено как отправленное."
                )

    except Exception as e:
        logger.error(f"Ошибка при отправке рассылки: {e}")


async def send_message(bot, user, text):
    try:
        await bot.send_message(chat_id=user.telegram_id, text=text)
    except Exception as e:
        raise e


def start_scheduler(bot, session_factory):
    scheduler.add_job(
        send_broadcast_messages,
        "interval",
        minutes=60,
        args=[bot, session_factory],
    )
    scheduler.start()
    logger.info("Scheduler запущен.")
