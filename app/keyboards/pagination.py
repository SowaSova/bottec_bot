from aiogram.types import InlineKeyboardButton
from core.pagination import Pagination


def get_pagination_buttons(
    current_page: int,
    total_items: int,
    items_per_page: int,
    level: str,
    parent_id: int = None,
) -> list:
    """
    Создает список кнопок пагинации (вперед и назад).

    :param current_page: Текущая страница.
    :param total_items: Общее количество элементов.
    :param items_per_page: Количество элементов на странице.
    :param level: Уровень пагинации ('category' или 'subcategory').
    :param parent_id: Идентификатор родительской категории (для подкатегорий).
    :return: Список InlineKeyboardButton.
    """
    buttons = []

    # Кнопка "Назад"
    if current_page > 0:
        pagination_back = Pagination(
            level=level, page=current_page - 1, parent_id=parent_id
        )
        buttons.append(
            InlineKeyboardButton(text="⬅️", callback_data=pagination_back.pack())
        )

    # Кнопка "Вперед"
    if (current_page + 1) * items_per_page < total_items:
        pagination_forward = Pagination(
            level=level, page=current_page + 1, parent_id=parent_id
        )
        buttons.append(
            InlineKeyboardButton(
                text="➡️", callback_data=pagination_forward.pack()
            )
        )

    return buttons


def get_back_button(level: str, parent_id: int = None) -> InlineKeyboardButton:
    """
    Создает кнопку "⬅️ Назад" для возврата на предыдущий уровень.

    :param level: Родительский уровень ('category').
    :param parent_id: Идентификатор родительской категории.
    :return: Объект InlineKeyboardButton.
    """
    pagination = Pagination(level=level, page=0, parent_id=parent_id)
    return InlineKeyboardButton(text="⬅️ Назад", callback_data=pagination.pack())
