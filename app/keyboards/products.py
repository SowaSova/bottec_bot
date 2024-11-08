# handlers/utils.py
import logging

from aiogram import html
from aiogram.types import CallbackQuery, InlineKeyboardButton, URLInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from core.constants import ITEMS_PER_PAGE
from core.pagination import Pagination

logger = logging.getLogger(__name__)


async def send_products_page(
    callback_query: CallbackQuery,
    products: list,
    subcategory_id: int,
    page: int,
    s3_service,
):
    """
    Отправляет продукты для определенной страницы.

    :param callback_query: Объект CallbackQuery.
    :param products: Список всех продуктов.
    :param subcategory_id: Идентификатор подкатегории.
    :param page: Текущая страница.
    :param s3_service: Сервис для получения URL изображений.
    """
    start_offset = page * ITEMS_PER_PAGE
    end_offset = start_offset + ITEMS_PER_PAGE
    paginated_products = products[start_offset:end_offset]

    for product in paginated_products:
        builder = InlineKeyboardBuilder()
        builder.button(text="🛒 Купить", callback_data=f"product_{product.id}")
        keyboard = builder.as_markup()
        message = (
            f"{html.bold(product.title)}\n"
            f"{html.italic(product.description)}\n"
            f"Цена: {product.price}"
        )
        image_relative_path = product.image
        try:
            presigned_url = await s3_service.get_object_url(image_relative_path)
        except Exception as e:
            logger.error(
                f"Ошибка при получении URL изображения для продукта {product.id}: {e}"
            )
            presigned_url = None

        if presigned_url:
            photo = URLInputFile(presigned_url)
            await callback_query.message.answer_photo(
                photo=photo, caption=message, reply_markup=keyboard
            )
        else:
            await callback_query.message.answer(
                "Изображение не доступно.", reply_markup=keyboard
            )

    # Определяем общее количество страниц
    total_products = len(products)
    total_pages = (total_products + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

    builder = InlineKeyboardBuilder()
    buttons_row = []

    # Кнопка "➡️ Далее"
    if page < total_pages - 1:
        pagination_forward = Pagination(
            level="product", page=page + 1, parent_id=subcategory_id
        ).pack()
        buttons_row.append(
            InlineKeyboardButton(
                text="➡️ Далее", callback_data=pagination_forward
            )
        )

    # Кнопка "⬅️ Назад"
    if page > 0:
        pagination_back = Pagination(
            level="product", page=page - 1, parent_id=subcategory_id
        ).pack()
        buttons_row.append(
            InlineKeyboardButton(text="⬅️ Назад", callback_data=pagination_back)
        )

    if buttons_row:
        builder.row(*buttons_row)
        pagination_keyboard = builder.as_markup()
        await callback_query.message.answer(
            f"Страница {page + 1} из {total_pages}",
            reply_markup=pagination_keyboard,
        )
