from aiogram import Bot, F, Router, html
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, PreCheckoutQuery
from core.config import settings
from keyboards.buy import get_confirm_button
from services.carts import CartItemService, CartService
from services.orders import OrderService
from services.products import ProductService
from services.users import UserService
from states.cart_state import CartStates
from utils.order_to_excel import log_order_to_excel

router = Router()


@router.callback_query(lambda c: c.data.startswith("product_"))
async def buy_product(
    callback_query: CallbackQuery, session, state: FSMContext
):
    product_id = int(callback_query.data.split("_")[1])
    await state.update_data(product_id=product_id)

    await callback_query.message.answer(
        "Введите количество товара, которое вы хотите добавить в корзину:",
        reply_markup=None,
    )

    await state.set_state(CartStates.WaitingForQuantity)

    await callback_query.answer()


@router.message(CartStates.WaitingForQuantity)
async def process_quantity(message: Message, session, state: FSMContext):
    data = await state.get_data()
    product_id = data.get("product_id")

    try:
        quantity = int(message.text)
        if quantity <= 0:
            raise ValueError("Количество должно быть положительным числом.")
    except ValueError:
        await message.reply(
            "Пожалуйста, введите корректное количество (целое число больше 0)."
        )
        return

    # Получаем информацию о продукте для подтверждения
    product_service = ProductService(session)
    product = await product_service.get_product_by_id(product_id)
    if not product:
        await message.reply("Выбранный товар не найден.")
        await state.clear()
        return

    total_price = product.price * quantity

    # Сохраняем количество в состоянии
    await state.update_data(quantity=quantity)

    # Используем функцию для создания клавиатуры
    keyboard = get_confirm_button()

    message_text = (
        f"Вы выбрали:\n"
        f"{html.bold(product.title)}\n"
        f"Количество: {quantity}\n"
        f"Цена за единицу: {product.price}\n"
        f"Итого: {total_price}"
    )

    await message.reply(message_text, reply_markup=keyboard, parse_mode="HTML")

    # Устанавливаем состояние ожидания подтверждения
    await state.set_state(CartStates.WaitingForConfirmation)


@router.callback_query(lambda c: c.data == "confirm_add")
async def confirm_add(
    callback_query: CallbackQuery, session, state: FSMContext
):
    data = await state.get_data()
    product_id = data.get("product_id")
    quantity = data.get("quantity")
    tg_user_id = callback_query.from_user.id

    user_service = UserService(session)
    user_id = await user_service.get_user_id_by_telegram_id(str(tg_user_id))

    # Инициализируем сервисы
    cart_service = CartService(session)
    cart_item_service = CartItemService(session)

    # Получаем или создаем корзину пользователя
    cart = await cart_service.get_or_create_cart(user_id)

    # Добавляем или обновляем товар в корзине
    await cart_item_service.add_or_update_item(cart.id, product_id, quantity)

    # Получаем информацию о продукте для отображения
    product_service = ProductService(session)
    product = await product_service.get_product_by_id(product_id)
    if not product:
        product_title = "Неизвестный товар"
    else:
        product_title = product.title

    await callback_query.message.answer(
        f"Товар <b>{product_title}</b> добавлен в корзину. Количество: {quantity}.",
        parse_mode="HTML",
    )

    # Сбрасываем состояние
    await state.clear()

    # Ответ на callback_query
    await callback_query.answer()


@router.callback_query(lambda c: c.data == "confirm_order")
async def confirm_order(
    callback_query: CallbackQuery, session, state: FSMContext
):
    tg_user_id = callback_query.from_user.id
    user_service = UserService(session)
    user_id = await user_service.get_user_id_by_telegram_id(str(tg_user_id))

    cart_service = CartService(session)
    cart_item_service = CartItemService(session)

    cart = await cart_service.get_or_create_cart(user_id)
    items = await cart_item_service.get_items(cart.id)

    if not items:
        await callback_query.message.answer("Ваша корзина пуста.")
        await callback_query.answer()
        return

    await callback_query.message.answer(
        "📦 Пожалуйста, введите адрес доставки:"
    )
    await state.set_state(CartStates.WaitingForDeliveryAddress)
    await callback_query.answer()


@router.message(CartStates.WaitingForDeliveryAddress)
async def process_delivery_address(
    message: Message, session, bot: Bot, state: FSMContext
):
    address = message.text.strip()

    if not address:
        await message.reply("❌ Пожалуйста, введите корректный адрес доставки.")
        return

    tg_user_id = message.from_user.id
    user_service = UserService(session)
    user_id = await user_service.get_user_id_by_telegram_id(str(tg_user_id))

    cart_service = CartService(session)
    cart_item_service = CartItemService(session)

    cart = await cart_service.get_or_create_cart(user_id)
    items = await cart_item_service.get_items(cart.id)

    if not items:
        await message.reply("❌ Ваша корзина пуста.")
        await state.clear()
        return
    order_service = OrderService(session)
    order = await order_service.create_order(user_id, address, items)
    await log_order_to_excel(session, order.id)

    await cart_item_service.clear_cart(cart.id)
    total_cost = sum(item.product.price * item.quantity for item in items)
    await bot.send_invoice(
        message.from_user.id,
        title="Подтверждение заказа",
        description="Подтверждение заказа",
        payload="confirm_order",
        provider_token=settings.YOOKASSA_TOKEN,
        currency="RUB",
        start_parameter="test_bot",
        prices=[
            {"label": "Руб", "amount": total_cost * 100}
        ],  # Обратите внимание на формат цены
    )

    await state.clear()


@router.pre_checkout_query()
async def pre_checkout_query_handler(
    pre_checkout_query: PreCheckoutQuery, bot: Bot
):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@router.message(F.successful_payment)
async def successful_payment_handler(message: Message, session):
    if message.successful_payment.invoice_payload != "confirm_order":
        await message.reply("❌ Ошибка при оплате. Попробуйте еще раз.")
    await message.reply("✅ Заказ успешно оформлен. Спасибо за покупку!")
