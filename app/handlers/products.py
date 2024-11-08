import logging

from aiogram import Router
from aiogram.types import CallbackQuery
from keyboards.products import send_products_page
from services.products import ProductService

router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(lambda c: c.data.startswith("subcategory_"))
async def show_products(callback_query: CallbackQuery, session, s3_service):
    """
    Обработчик для отображения продуктов в выбранной подкатегории с пагинацией.
    """
    try:
        subcategory_id = int(callback_query.data.split("_")[1])
        product_service = ProductService(session)
        products = await product_service.get_products(subcategory_id)

        if not products:
            await callback_query.message.edit_text("Продукты не найдены.")
            await callback_query.answer()
            return

        # Отправляем первую страницу продуктов
        await send_products_page(
            callback_query=callback_query,
            products=products,
            subcategory_id=subcategory_id,
            page=0,
            s3_service=s3_service,
        )

        await callback_query.answer()
        logger.info(
            f"User {callback_query.from_user.id} viewed products in subcategory {subcategory_id}, page 0"
        )
    except Exception as e:
        logger.error(f"Error in show_products: {e}")
        await callback_query.message.reply(
            "Произошла ошибка при отображении продуктов."
        )
        await callback_query.answer()
