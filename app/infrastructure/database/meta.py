from infrastructure.database.orm import Base
from sqlalchemy import Column, Integer


class BaseDBModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
