import urllib.parse

from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PWD: SecretStr

    REDIS_HOST: str
    REDIS_PORT: int

    MINIO_HOST: str
    MINIO_PORT: str
    MINIO_SSL: bool

    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: SecretStr
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: SecretStr
    MINIO_BUCKET: str

    BOT_TOKEN: str

    YOOKASSA_TOKEN: str

    LOG_DIR: str = "logs"
    LOG_FILE: str = "bot.log"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def DB_URL(self):
        pwd = self.DB_PWD.get_secret_value()
        return f"postgresql+asyncpg://{self.DB_USER}:{urllib.parse.quote_plus(pwd)}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def REDIS_URL(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    @property
    def MINIO_URL(self):
        return f"{self.MINIO_HOST}:{self.MINIO_PORT}"


settings = Settings()
