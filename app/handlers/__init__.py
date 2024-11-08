# app/handlers/__init__.py

from aiogram import Dispatcher

from .buy import router as buy_router
from .cart import router as cart_router
from .categories import router as catalog_router
from .faq import router as faq_router
from .pagination import router as pagination_router
from .products import router as products_router
from .start import router as start_router
from .subscriptions import router as subscription_router


def register_all_handlers(dp: Dispatcher):
    dp.include_router(start_router)
    dp.include_router(subscription_router)
    dp.include_router(catalog_router)
    dp.include_router(pagination_router)
    dp.include_router(products_router)
    dp.include_router(buy_router)
    dp.include_router(cart_router)
    dp.include_router(faq_router)
