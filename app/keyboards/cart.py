from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_remove_button(
    product_title: str, product_id: int
) -> InlineKeyboardMarkup:
    """
    Создает кнопку "❌ Удалить" для конкретного товара.

    :param product_title: Название продукта.
    :param product_id: Идентификатор продукта.
    :return: Объект InlineKeyboardMarkup с кнопкой удаления.
    """
    remove_button = InlineKeyboardButton(
        text=f"❌ Удалить {product_title}", callback_data=f"remove_{product_id}"
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[remove_button]])
    return keyboard


def get_remove_button_generic(product_id: int) -> InlineKeyboardMarkup:
    """
    Создает общую кнопку "❌ Удалить" для конкретного товара без названия.

    :param product_id: Идентификатор продукта.
    :return: Объект InlineKeyboardMarkup с кнопкой удаления.
    """
    remove_button = InlineKeyboardButton(
        text="❌ Удалить", callback_data=f"remove_{product_id}"
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[remove_button]])
    return keyboard


def get_confirm_order_button() -> InlineKeyboardMarkup:
    """
    Создает кнопку "✅ Подтвердить заказ".

    :return: Объект InlineKeyboardMarkup с кнопкой подтверждения заказа.
    """
    confirm_button = InlineKeyboardButton(
        text="✅ Подтвердить заказ", callback_data="confirm_order"
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[confirm_button]])
    return keyboard


def get_cart_keyboard(items: list) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру для отображения корзины с кнопками удаления для каждого товара
    и кнопкой подтверждения заказа.

    :param items: Список товаров в корзине.
    :return: Объект InlineKeyboardMarkup с кнопками.
    """
    builder = InlineKeyboardBuilder()
    for item in items:
        remove_button = InlineKeyboardButton(
            text=f"❌ Удалить {item.product.title}",
            callback_data=f"remove_{item.product_id}",
        )
        builder.row(remove_button)
    confirm_button = InlineKeyboardButton(
        text="✅ Подтвердить заказ", callback_data="confirm_order"
    )
    builder.row(confirm_button)
    keyboard = builder.as_markup()
    return keyboard
