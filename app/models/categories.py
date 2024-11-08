from infrastructure.database.meta import BaseDBModel
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Category(BaseDBModel):
    __tablename__ = "catalog_category"

    title = Column(String(200), nullable=False)
    slug = Column(String(200), nullable=False, unique=True)
    parent_id = Column(
        Integer, ForeignKey("catalog_category.id"), nullable=True
    )

    parent = relationship(
        "Category", remote_side="Category.id", back_populates="children"
    )
    children = relationship(
        "Category", back_populates="parent", cascade="all, delete-orphan"
    )

    products = relationship(
        "Product", back_populates="category", cascade="all, delete-orphan"
    )
