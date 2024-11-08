from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_confirm_button():
    """
    Создает клавиатуру с кнопкой "✅ Подтвердить".
    """
    confirm_button = InlineKeyboardButton(
        text="✅ Подтвердить", callback_data="confirm_add"
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[confirm_button]])
    return keyboard


def get_empty_cart_keyboard():
    """
    Создает клавиатуру для пустой корзины (можно добавить дополнительные кнопки при необходимости).
    """
    # Пример: кнопка "Вернуться в магазин"
    return InlineKeyboardMarkup()


def get_order_confirmation_keyboard():
    """
    Создает клавиатуру для подтверждения заказа.
    """
    confirm_order_button = InlineKeyboardButton(
        text="✅ Подтвердить заказ", callback_data="confirm_order"
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[confirm_order_button]])
    return keyboard
