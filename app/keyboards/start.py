from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_main_keyboard():
    catalog = InlineKeyboardButton(text="📖 Каталог", callback_data="catalog")
    cart = InlineKeyboardButton(text="🛒 Корзина", callback_data="cart")
    faq = InlineKeyboardButton(text="❓ FAQ", callback_data="faq")

    inline_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [catalog],
            [cart],
            [faq],
        ],
    )
    return inline_keyboard
