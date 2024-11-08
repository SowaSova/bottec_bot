from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from core.pagination import Pagination


def get_catalog_keyboard(
    items: list,
    page: int,
    items_per_page: int,
    level: str,
    parent_id: int = None,
) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру для отображения списка категорий или подкатегорий с пагинацией.

    :param items: Список элементов (категорий или подкатегорий).
    :param page: Текущая страница.
    :param items_per_page: Количество элементов на странице.
    :param level: Уровень ('category' или 'subcategory').
    :param parent_id: Идентификатор родительской категории (для подкатегорий).
    :return: Объект InlineKeyboardMarkup с кнопками элементов и пагинации.
    """
    builder = InlineKeyboardBuilder()
    start_offset = page * items_per_page
    end_offset = start_offset + items_per_page
    paginated_items = items[start_offset:end_offset]

    # Добавляем кнопки для каждого элемента
    for item in paginated_items:
        callback_data_str = f"{level}_{item.id}"
        button = InlineKeyboardButton(
            text=item.title, callback_data=callback_data_str
        )
        builder.add(button)  # Каждая кнопка в отдельной строке

    # Добавляем кнопки пагинации
    if len(items) > end_offset or page > 0:
        pagination_buttons = []
        if page > 0:
            pagination_back = Pagination(
                level=level, page=page - 1, parent_id=parent_id
            ).pack()
            pagination_buttons.append(
                InlineKeyboardButton(
                    text="⬅️ Назад", callback_data=pagination_back
                )
            )
        if len(items) > end_offset:
            pagination_forward = Pagination(
                level=level, page=page + 1, parent_id=parent_id
            ).pack()
            pagination_buttons.append(
                InlineKeyboardButton(
                    text="➡️ Далее", callback_data=pagination_forward
                )
            )
        builder.row(*pagination_buttons)

    return builder.as_markup()
