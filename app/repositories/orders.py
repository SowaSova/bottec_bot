# repositories/orders.py
from core.constants import ORDER_STATUSES
from models.orders import Order, OrderItem
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload


class OrderRepository:
    def __init__(self, session):
        self.session = session
        self.model = Order

    async def create_order(self, user_id: int, delivery_address: str) -> Order:
        new_order = self.model(
            user_id=user_id,
            delivery_address=delivery_address,
            status=ORDER_STATUSES["new"],
        )
        self.session.add(new_order)
        await self.session.commit()
        await self.session.refresh(new_order)
        return new_order

    async def get_order_by_id(self, order_id: int) -> Order:
        stmt = (
            select(self.model)
            .where(self.model.id == order_id)
            .options(selectinload(self.model.user))
        )
        result = await self.session.execute(stmt)
        order = result.scalars().first()
        return order


class OrderItemRepository:
    def __init__(self, session):
        self.session = session
        self.model = OrderItem

    async def create_order_item(
        self, order_id: int, product_id: int, quantity: int, price: float
    ) -> OrderItem:
        new_order_item = self.model(
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
            price=price,
        )
        self.session.add(new_order_item)
        await self.session.commit()
        await self.session.refresh(new_order_item)
        return new_order_item

    async def get_order_items_by_order_id(self, order_id: int):
        stmt = (
            select(self.model)
            .where(self.model.order_id == order_id)
            .options(
                selectinload(self.model.product), selectinload(self.model.order)
            )
        )
        result = await self.session.execute(stmt)
        order_items = result.scalars().all()
        return order_items
