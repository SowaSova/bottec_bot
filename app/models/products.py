from infrastructure.database.meta import BaseDBModel
from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import relationship


class Product(BaseDBModel):
    __tablename__ = "catalog_product"

    title = Column(String(200), nullable=False)
    slug = Column(String(200), nullable=False, unique=True)
    image = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    is_available = Column(Boolean, default=True, nullable=False)

    category_id = Column(
        Integer, ForeignKey("catalog_category.id"), nullable=False
    )
    category = relationship("Category", back_populates="products")
