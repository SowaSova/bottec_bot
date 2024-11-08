# handlers/pagination.py
import logging

from aiogram import Router
from aiogram.types import CallbackQuery
from core.constants import ITEMS_PER_PAGE
from core.pagination import Pagination
from keyboards.categories import get_catalog_keyboard
from keyboards.products import send_products_page
from services.categories import CategoryService
from services.products import ProductService

router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(Pagination.filter())
async def handle_pagination(
    callback_query: CallbackQuery,
    callback_data: Pagination,
    session,
    s3_service,
):
    """
    Обработчик для обработки пагинации и выбора категорий/подкатегорий/products.
    """
    try:
        page = callback_data.page
        level = callback_data.level
        parent_id = callback_data.parent_id

        if level == "category":
            # Обработка пагинации для категорий
            category_service = CategoryService(session)
            categories = await category_service.get_root_categories()
            if not categories:
                await callback_query.message.edit_text("Категории не найдены.")
                await callback_query.answer()
                return

            keyboard = get_catalog_keyboard(
                items=categories,
                page=page,
                items_per_page=ITEMS_PER_PAGE,
                level="category",
            )
            await callback_query.message.edit_text(
                "📂 <b>Каталог товаров:</b>",
                reply_markup=keyboard,
                parse_mode="HTML",
            )
            logger.info(
                f"User {callback_query.from_user.id} navigated to catalog page {page}"
            )

        elif level == "subcategory":
            # Обработка пагинации для подкатегорий
            category_service = CategoryService(session)
            subcategories = await category_service.get_subcategories(parent_id)
            if not subcategories:
                await callback_query.message.edit_text(
                    "Подкатегории не найдены."
                )
                await callback_query.answer()
                return

            keyboard = get_catalog_keyboard(
                items=subcategories,
                page=page,
                items_per_page=ITEMS_PER_PAGE,
                level="subcategory",
                parent_id=parent_id,
            )
            await callback_query.message.edit_text(
                "📂 <b>Подкатегории:</b>",
                reply_markup=keyboard,
                parse_mode="HTML",
            )
            logger.info(
                f"User {callback_query.from_user.id} navigated to subcategory {parent_id} page {page}"
            )

        elif level == "product":
            # Обработка пагинации для продуктов
            subcategory_id = parent_id
            product_service = ProductService(session)
            products = await product_service.get_products(subcategory_id)

            if not products:
                await callback_query.message.edit_text("Продукты не найдены.")
                await callback_query.answer()
                return

            await send_products_page(
                callback_query=callback_query,
                products=products,
                subcategory_id=subcategory_id,
                page=page,
                s3_service=s3_service,
            )

            logger.info(
                f"User {callback_query.from_user.id} navigated to product page {page} in subcategory {subcategory_id}"
            )

        await callback_query.answer()
    except Exception as e:
        logger.error(f"Error in handle_pagination: {e}")
        await callback_query.message.reply(
            "Произошла ошибка при обработке запроса."
        )
        await callback_query.answer()
