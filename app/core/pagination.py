# core/pagination.py
from typing import Optional

from aiogram.filters.callback_data import CallbackData


class Pagination(CallbackData, prefix="pag"):
    level: str
    page: int
    parent_id: Optional[int] = None
