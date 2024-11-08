from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from infrastructure.database.orm import AsyncSessionLocal


class DbSessionMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: TelegramObject, data: dict):
        async with AsyncSessionLocal() as session:
            data["session"] = session
            return await handler(event, data)
