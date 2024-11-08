from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery
from core.config import settings
from services.s3 import S3Service


class S3Middleware(BaseMiddleware):
    def __init__(self):
        super().__init__()
        self.s3_service = S3Service(
            settings.MINIO_SECRET_KEY.get_secret_value(),
            settings.MINIO_ACCESS_KEY,
            settings.MINIO_BUCKET,
            settings.MINIO_SSL,
        )

    async def __call__(self, handler, event, data):
        data["s3_service"] = self.s3_service
        await handler(event, data)

    async def on_pre_process_callback_query(
        self, callback_query: CallbackQuery, data: dict
    ):
        data["s3_service"] = self.s3_service
