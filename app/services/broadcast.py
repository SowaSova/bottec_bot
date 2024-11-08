import logging
from typing import List

from models.broadcast import BroadcastMessage
from repositories.broadcast import BroadcastMessageRepository

logger = logging.getLogger(__name__)


class BroadcastMessageService:
    def __init__(self, session):
        self.session = session
        self.repository = BroadcastMessageRepository(session)

    async def get_messages(self) -> List[BroadcastMessage]:
        logger.info("Запрос на получение ожидающих сообщений для рассылки.")
        return await self.repository.get_messages()

    async def mark_as_sent(self, message: BroadcastMessage) -> None:
        try:
            await self.repository.mark_as_sent(message)
            logger.info(
                f"Сообщение с ID {message.id} успешно отправлено и отмечено как отправленное."
            )
        except Exception as e:
            logger.error(
                f"Не удалось отправить сообщение с ID {message.id}: {e}"
            )
            raise
