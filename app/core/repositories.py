# repositories/base.py
import logging
from typing import Generic, List, Optional, Type, TypeVar

from infrastructure.database.meta import Base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

T = TypeVar("T", bound=Base)

logger = logging.getLogger(__name__)


class BaseRepository(Generic[T]):
    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model

    async def get_all(self) -> List[T]:
        try:
            stmt = select(self.model)
            result = await self.session.execute(stmt)
            items = result.scalars().all()
            logger.debug(
                f"Получено {len(items)} элементов модели {self.model.__name__}."
            )
            return items
        except SQLAlchemyError as e:
            logger.error(
                f"Ошибка при получении всех элементов модели {self.model.__name__}: {e}"
            )
            raise

    async def get_by_id(self, id: int) -> Optional[T]:
        try:
            stmt = select(self.model).where(self.model.id == id)
            result = await self.session.execute(stmt)
            item = result.scalars().first()
            logger.debug(
                f"Получен элемент модели {self.model.__name__} с ID {id}: {item}."
            )
            return item
        except SQLAlchemyError as e:
            logger.error(
                f"Ошибка при получении элемента модели {self.model.__name__} с ID {id}: {e}"
            )
            raise

    async def add(self, obj: T) -> None:
        try:
            self.session.add(obj)
            await self.session.commit()
            await self.session.refresh(obj)
            logger.debug(
                f"Добавлен элемент модели {self.model.__name__} с ID {obj.id}."
            )
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(
                f"Ошибка при добавлении элемента модели {self.model.__name__}: {e}"
            )
            raise

    async def delete(self, obj: T) -> None:
        try:
            await self.session.delete(obj)
            await self.session.commit()
            logger.debug(
                f"Удалён элемент модели {self.model.__name__} с ID {obj.id}."
            )
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(
                f"Ошибка при удалении элемента модели {self.model.__name__} с ID {obj.id}: {e}"
            )
            raise
