from repositories.orders import OrderItemRepository, OrderRepository


class OrderService:
    def __init__(self, session):
        self.session = session
        self.order_repository = OrderRepository(session)
        self.order_item_repository = OrderItemRepository(session)

    async def create_order(
        self, user_id: int, delivery_address: str, items: list
    ):
        order = await self.order_repository.create_order(
            user_id, delivery_address
        )
        for item in items:
            await self.order_item_repository.create_order_item(
                order.id, item.product_id, item.quantity, item.product.price
            )
        return order

    async def get_order_by_id(self, order_id: int):
        return await self.order_repository.get_order_by_id(order_id)


class OrderItemService:
    def __init__(self, session):
        self.session = session
        self.repository = OrderItemRepository(session)

    async def get_order_items_by_order_id(self, order_id: int):
        return await self.repository.get_order_items_by_order_id(order_id)
