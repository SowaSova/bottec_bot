# repositories/broadcast.py
import logging
from datetime import datetime
from typing import List

from models.broadcast import BroadcastMessage
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class BroadcastMessageRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.model = BroadcastMessage

    async def get_messages(self) -> List[BroadcastMessage]:
        try:
            stmt = select(self.model).where(
                self.model.is_sent == False,
                self.model.scheduled_time <= datetime.now(tz=None),
            )
            result = await self.session.execute(stmt)
            messages = result.scalars().all()
            logger.debug(f"Получено {len(messages)} сообщений для рассылки.")
            return messages
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при получении сообщений для рассылки: {e}")
            raise

    async def mark_as_sent(self, message: BroadcastMessage) -> None:
        try:
            message.is_sent = True
            self.session.add(message)
            await self.session.commit()
            logger.debug(
                f"Сообщение с ID {message.id} помечено как отправленное."
            )
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Ошибка при отметке сообщения как отправленного: {e}")
            raise
