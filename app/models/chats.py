from infrastructure.database.meta import BaseDBModel
from sqlalchemy import Column, String


class RequiredChat(BaseDBModel):
    __tablename__ = "chats_requiredchat"

    chat_id = Column(String(30), nullable=False, unique=True)
    title = Column(String(255), unique=True, nullable=False)
    username = Column(String(255), nullable=True)
    type = Column(String(30), nullable=False)
