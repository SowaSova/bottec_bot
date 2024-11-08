# handlers/categories.py
import logging

from aiogram import Router
from aiogram.types import CallbackQuery
from core.constants import ITEMS_PER_PAGE
from keyboards.categories import get_catalog_keyboard
from services.categories import CategoryService

logger = logging.getLogger(__name__)

router = Router()


@router.callback_query(lambda c: c.data == "catalog")
async def show_categories(
    callback_query: CallbackQuery, session, page: int = 0
):
    """
    Обработчик для отображения корневых категорий каталога.
    """
    try:
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
        await callback_query.answer()
        logger.info(
            f"User {callback_query.from_user.id} viewed catalog page {page}"
        )
    except Exception as e:
        logger.error(f"Error in show_categories: {e}")
        await callback_query.message.reply(
            "Произошла ошибка при отображении каталога."
        )
        await callback_query.answer()


@router.callback_query(lambda c: c.data.startswith("category_"))
async def show_subcategories(callback_query: CallbackQuery, session):
    """
    Обработчик для отображения подкатегорий выбранной категории.
    """
    try:
        category_id = int(callback_query.data.split("_")[1])
        await display_subcategories(
            callback_query, session, category_id, page=0
        )
        logger.info(
            f"User {callback_query.from_user.id} viewed subcategories of category {category_id}, page 0"
        )
    except (ValueError, IndexError) as e:
        logger.error(f"Error parsing category_id: {e}")
        await callback_query.message.reply(
            "Произошла ошибка при выборе категории."
        )
        await callback_query.answer()


async def display_subcategories(
    callback_query: CallbackQuery, session, category_id: int, page: int = 0
):
    """
    Отображает подкатегории выбранной категории с пагинацией.
    """
    try:
        category_service = CategoryService(session)
        subcategories = await category_service.get_subcategories(category_id)

        if not subcategories:
            await callback_query.message.edit_text("Подкатегории не найдены.")
            await callback_query.answer()
            return

        keyboard = get_catalog_keyboard(
            items=subcategories,
            page=page,
            items_per_page=ITEMS_PER_PAGE,
            level="subcategory",
            parent_id=category_id,
        )

        await callback_query.message.edit_text(
            "📂 <b>Подкатегории:</b>", reply_markup=keyboard, parse_mode="HTML"
        )
        await callback_query.answer()
    except Exception as e:
        logger.error(f"Error in display_subcategories: {e}")
        await callback_query.message.reply(
            "Произошла ошибка при отображении подкатегорий."
        )
        await callback_query.answer()
