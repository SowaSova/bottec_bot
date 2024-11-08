from infrastructure.database.meta import BaseDBModel
from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class TelegramUser(BaseDBModel):
    __tablename__ = "users_telegramuser"

    username = Column(String(255), nullable=True)
    telegram_id = Column(String(20), unique=True, nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    carts = relationship(
        "Cart", back_populates="user", cascade="all, delete-orphan"
    )
    orders = relationship(
        "Order", back_populates="user", cascade="all, delete-orphan"
    )
