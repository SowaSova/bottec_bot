from infrastructure.database.meta import BaseDBModel
from sqlalchemy import Column, String


class FAQ(BaseDBModel):
    __tablename__ = "chats_faq"

    question = Column(String(255), nullable=False)
    answer = Column(String(255), nullable=False)
