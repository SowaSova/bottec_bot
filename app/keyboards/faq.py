# keyboards/faq_keyboards.py
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_faq_instruction_keyboard() -> InlineKeyboardMarkup:
    """
    Создает клавиатуру с кнопкой для доступа к FAQ.

    :return: InlineKeyboardMarkup с кнопкой "FAQ".
    """
    builder = InlineKeyboardBuilder()

    faq_button = InlineKeyboardButton(
        text="🔍 FAQ", callback_data="faq_instructions"
    )
    builder.add(faq_button)  # Каждая кнопка в отдельной строке

    return builder.as_markup()
