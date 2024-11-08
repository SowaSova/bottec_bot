from core.config import settings
from infrastructure.s3.client import S3Client


class S3Service:
    def __init__(
        self, secret_key: str, access_key: str, bucket_name: str, secure: bool
    ):
        self.bucket_name = bucket_name
        self.s3_client = S3Client(access_key, secret_key, secure)
        self.s3_admin = S3Client(
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY.get_secret_value(),
            secure=settings.MINIO_SSL,
        )

    async def get_object_url(self, url: str) -> str:
        object_key = url
        return await self.s3_client.get_presigned_url(
            bucket_name=self.bucket_name, object_name=object_key
        )
