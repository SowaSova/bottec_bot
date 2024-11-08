from infrastructure.database.meta import BaseDBModel
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Order(BaseDBModel):
    __tablename__ = "orders_order"

    user_id = Column(
        Integer, ForeignKey("users_telegramuser.id"), nullable=False
    )
    delivery_address = Column(String(255), nullable=False)
    status = Column(String(30), nullable=False, default="new")
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user = relationship("TelegramUser", back_populates="orders")
    items = relationship(
        "OrderItem", back_populates="order", cascade="all, delete-orphan"
    )


class OrderItem(BaseDBModel):
    __tablename__ = "orders_orderitem"

    order_id = Column(Integer, ForeignKey("orders_order.id"), nullable=False)
    product_id = Column(
        Integer, ForeignKey("catalog_product.id"), nullable=False
    )
    quantity = Column(Integer, default=1, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)

    product = relationship("Product")
    order = relationship("Order", back_populates="items")
