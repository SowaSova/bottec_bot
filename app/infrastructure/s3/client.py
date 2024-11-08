from contextlib import asynccontextmanager
from datetime import timedelta

from aiobotocore.session import get_session
from core.config import settings


class S3Client:
    """
    Класс для работы MinIO API обычным пользователем
    Необходим для:
    - создание бакетов
    - загрузка файлов
    - удаление бакетов
    - удаление файлов
    """

    def __init__(
        self,
        access_key: str,
        secret_key: str,
        secure: bool,
    ):
        self.protocol = "https://" if secure else "http://"
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": self.protocol + settings.MINIO_URL,
        }
        # self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_s3_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def get_presigned_url(
        self, bucket_name: str, object_name: str
    ) -> str:
        async with self.get_s3_client() as client:
            expiration = timedelta(hours=1)
            url = await client.generate_presigned_url(
                ClientMethod="get_object",
                Params={"Bucket": bucket_name, "Key": object_name},
                ExpiresIn=int(expiration.total_seconds()),
            )
            return url
