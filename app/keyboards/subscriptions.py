from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_subscription_keyboard(
    not_subscribed_chats: list,
) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру с кнопками для неподписанных чатов и кнопкой "Проверить подписку".

    :param not_subscribed_chats: Список чатов, на которые пользователь не подписан.
    :param subcategory_id: Идентификатор подкатегории (используется как parent_id для Pagination).
    :return: Объект InlineKeyboardMarkup с кнопками.
    """
    builder = InlineKeyboardBuilder()

    for chat in not_subscribed_chats:
        link = chat.get("invite_link")
        if link:
            builder.button(text=chat["name"], url=link)

    builder.button(
        text="🔄 Проверить подписку", callback_data="check_subscription"
    )

    return builder.as_markup()
