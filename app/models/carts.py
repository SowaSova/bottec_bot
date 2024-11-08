from infrastructure.database.meta import BaseDBModel
from sqlalchemy import BigInteger, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship


class Cart(BaseDBModel):
    __tablename__ = "cart_cart"

    user_id = Column(
        BigInteger, ForeignKey("users_telegramuser.id"), nullable=False
    )

    user = relationship("TelegramUser", back_populates="carts")
    items = relationship(
        "CartItem", back_populates="cart", cascade="all, delete-orphan"
    )


class CartItem(BaseDBModel):
    __tablename__ = "cart_cartitem"

    cart_id = Column(BigInteger, ForeignKey("cart_cart.id"), nullable=False)
    product_id = Column(
        Integer, ForeignKey("catalog_product.id"), nullable=False
    )
    quantity = Column(Integer, default=1, nullable=False)

    cart = relationship("Cart", back_populates="items")
    product = relationship("Product")
