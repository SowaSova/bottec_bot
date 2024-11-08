from typing import Tuple

from aiogram import Router, html
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from keyboards.cart import get_cart_keyboard
from services.carts import CartItemService, CartService
from services.users import UserService

router = Router()


async def build_cart_message(items: list) -> Tuple[str, int]:
    """
    Формирует текст сообщения о содержимом корзины и вычисляет общую стоимость.

    :param items: Список товаров в корзине.
    :return: Кортеж из текста сообщения и общей стоимости.
    """
    message_text = "🛒 <b>Ваша корзина:</b>\n\n"
    total_cost = 0
    for item in items:
        product = item.product
        item_total = product.price * item.quantity
        total_cost += item_total
        message_text += (
            f"{html.bold(product.title)}\n"
            f"Количество: {item.quantity}\n"
            f"Цена за единицу: {product.price} руб.\n"
            f"Итого: {item_total} руб.\n\n"
        )
    message_text += f"<b>Общая сумма:</b> {total_cost} руб."
    return message_text, total_cost


@router.callback_query(lambda c: c.data == "cart")
async def show_cart(callback_query: CallbackQuery, session, state: FSMContext):
    tg_user_id = callback_query.from_user.id
    user_service = UserService(session)
    user_id = await user_service.get_user_id_by_telegram_id(str(tg_user_id))

    cart_service = CartService(session)
    cart_item_service = CartItemService(session)

    cart = await cart_service.get_or_create_cart(user_id)
    items = await cart_item_service.get_items(cart.id)

    if not items:
        await callback_query.message.reply("Ваша корзина пуста.")
        await callback_query.answer()
        return

    # Формирование текста сообщения и клавиатуры с кнопками "Удалить"
    message_text, total_cost = await build_cart_message(items)
    keyboard = get_cart_keyboard(items)

    await callback_query.message.reply(
        message_text, reply_markup=keyboard, parse_mode="HTML"
    )
    await callback_query.answer()


@router.callback_query(lambda c: c.data.startswith("remove_"))
async def remove_item(
    callback_query: CallbackQuery, session, state: FSMContext
):
    product_id = int(callback_query.data.split("_")[1])
    tg_user_id = callback_query.from_user.id
    user_service = UserService(session)
    user_id = await user_service.get_user_id_by_telegram_id(str(tg_user_id))

    cart_service = CartService(session)
    cart_item_service = CartItemService(session)

    cart = await cart_service.get_or_create_cart(user_id)
    await cart_item_service.remove_item(cart.id, product_id)

    # Получение обновленных данных корзины
    items = await cart_item_service.get_items(cart.id)

    if not items:
        await callback_query.message.edit_text("Ваша корзина пуста.")
        await callback_query.answer("Товар удален. Корзина пуста.")
        return

    # Формирование обновленного сообщения корзины
    message_text, total_cost = await build_cart_message(items)
    keyboard = get_cart_keyboard(items)

    await callback_query.message.edit_text(
        message_text, reply_markup=keyboard, parse_mode="HTML"
    )
    await callback_query.answer("Товар удален из корзины.")
