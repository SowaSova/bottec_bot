from infrastructure.database.meta import BaseDBModel
from sqlalchemy import Boolean, Column, DateTime, Text
from sqlalchemy.sql import func


class BroadcastMessage(BaseDBModel):
    __tablename__ = "broadcast_broadcastmessage"

    message_text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    scheduled_time = Column(DateTime(timezone=True))
    is_sent = Column(Boolean, default=False, nullable=False)
