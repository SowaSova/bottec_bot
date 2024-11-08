import logging

from models.carts import Cart
from repositories.carts import CartItemRepository, CartRepository

logger = logging.getLogger(__name__)


class CartService:
    def __init__(self, session):
        self.session = session
        self.repository = CartRepository(session)

    async def get_or_create_cart(self, user_id: int) -> Cart:
        logger.info(
            f"Получение или создание корзины для пользователя с ID: {user_id}"
        )
        cart = await self.repository.get_cart_by_user_id(user_id)
        if not cart:
            logger.info(
                f"Корзина для пользователя с ID: {user_id} не найдена, создается новая корзина"
            )
            cart = await self.repository.create_cart(user_id)
        return cart


class CartItemService:
    def __init__(self, session):
        self.session = session
        self.repository = CartItemRepository(session)

    async def get_items(self, cart_id: int):
        logger.info(
            f"Получение всех элементов корзины для корзины с ID: {cart_id}"
        )
        return await self.repository.get_items_by_cart_id(cart_id)

    async def add_or_update_item(
        self, cart_id: int, product_id: int, quantity: int
    ):
        logger.info(
            f"Добавление или обновление товара с ID: {product_id} в корзине с ID: {cart_id}"
        )
        item = await self.repository.get_item(cart_id, product_id)
        if item:
            logger.info(
                f"Товар с ID: {product_id} уже существует в корзине, обновляем количество"
            )
            await self.repository.update_item(item, quantity)
        else:
            logger.info(
                f"Товар с ID: {product_id} не найден в корзине, добавляем новый элемент"
            )
            await self.repository.add_item(cart_id, product_id, quantity)

    async def remove_item(self, cart_id: int, product_id: int):
        logger.info(
            f"Удаление товара с ID: {product_id} из корзины с ID: {cart_id}"
        )
        item = await self.repository.get_item(cart_id, product_id)
        if item:
            await self.repository.remove_item(cart_id, product_id)

    async def clear_cart(self, cart_id: int):
        logger.info(f"Очистка корзины с ID: {cart_id}")
        items = await self.repository.get_items_by_cart_id(cart_id)
        for item in items:
            logger.info(
                f"Удаление товара с ID: {item.product_id} из корзины с ID: {cart_id}"
            )
            await self.repository.remove_item(cart_id, item.product_id)
