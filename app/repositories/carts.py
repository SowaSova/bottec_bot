import logging

from models.carts import Cart, CartItem
from sqlalchemy import delete
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

logger = logging.getLogger(__name__)


class CartRepository:
    def __init__(self, session):
        self.session = session
        self.model = Cart

    async def get_cart_by_user_id(self, user_id: int) -> Cart:
        logger.info(f"Получение корзины для пользователя с ID: {user_id}")
        stmt = select(self.model).where(self.model.user_id == user_id)
        result = await self.session.execute(stmt)
        cart = result.scalars().first()
        if cart:
            logger.info(f"Корзина найдена для пользователя с ID: {user_id}")
        else:
            logger.info(f"Корзина не найдена для пользователя с ID: {user_id}")
        return cart

    async def create_cart(self, user_id: int) -> Cart:
        logger.info(f"Создание новой корзины для пользователя с ID: {user_id}")
        new_cart = self.model(user_id=user_id)
        self.session.add(new_cart)
        await self.session.commit()
        await self.session.refresh(new_cart)
        logger.info(f"Корзина создана для пользователя с ID: {user_id}")
        return new_cart


class CartItemRepository:
    def __init__(self, session):
        self.session = session
        self.model = CartItem

    async def get_items_by_cart_id(self, cart_id: int):
        logger.info(f"Получение элементов корзины для корзины с ID: {cart_id}")
        stmt = (
            select(self.model)
            .where(self.model.cart_id == cart_id)
            .options(selectinload(self.model.product))
        )
        result = await self.session.execute(stmt)
        items = result.scalars().all()
        logger.info(
            f"Найдено {len(items)} элементов для корзины с ID: {cart_id}"
        )
        return items

    async def get_item(self, cart_id: int, product_id: int) -> CartItem:
        logger.info(
            f"Получение элемента корзины с ID товара: {product_id} для корзины с ID: {cart_id}"
        )
        stmt = select(self.model).where(
            self.model.cart_id == cart_id, self.model.product_id == product_id
        )
        result = await self.session.execute(stmt)
        item = result.scalars().first()
        if item:
            logger.info(
                f"Элемент корзины найден: товар {product_id} в корзине {cart_id}"
            )
        else:
            logger.info(
                f"Элемент корзины не найден: товар {product_id} в корзине {cart_id}"
            )
        return item

    async def add_item(
        self, cart_id: int, product_id: int, quantity: int
    ) -> CartItem:
        logger.info(
            f"Добавление товара с ID: {product_id} в корзину с ID: {cart_id} в количестве {quantity}"
        )
        new_item = self.model(
            cart_id=cart_id, product_id=product_id, quantity=quantity
        )
        self.session.add(new_item)
        await self.session.commit()
        await self.session.refresh(new_item)
        logger.info(
            f"Товар с ID: {product_id} добавлен в корзину с ID: {cart_id}"
        )
        return new_item

    async def update_item(self, item: CartItem, quantity: int):
        logger.info(
            f"Обновление количества товара с ID: {item.product_id} в корзине с ID: {item.cart_id}"
        )
        item.quantity += quantity
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        logger.info(
            f"Количество товара с ID: {item.product_id} в корзине с ID: {item.cart_id} обновлено"
        )
        return item

    async def remove_item(self, cart_id: int, product_id: int):
        logger.info(
            f"Удаление товара с ID: {product_id} из корзины с ID: {cart_id}"
        )
        stmt = delete(self.model).where(
            self.model.cart_id == cart_id, self.model.product_id == product_id
        )
        await self.session.execute(stmt)
        await self.session.commit()
        logger.info(
            f"Товар с ID: {product_id} удален из корзины с ID: {cart_id}"
        )
