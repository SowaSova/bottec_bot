import asyncio
import os

import openpyxl
from openpyxl import Workbook
from services.orders import OrderItemService, OrderService
from sqlalchemy.ext.asyncio import AsyncSession

EXCEL_FILE_PATH = "orders.xlsx"


async def log_order_to_excel(session: AsyncSession, order_id: int):
    order_service = OrderService(session)
    order_items_service = OrderItemService(session)

    order = await order_service.get_order_by_id(order_id)
    order_items = await order_items_service.get_order_items_by_order_id(
        order_id
    )
    if not order:
        # Логирование ошибки или обработка случая, когда заказ не найден
        return

    # Подготовка данных для записи
    order_data = {
        "Order ID": order.id,
        "User ID": order.user_id,
        "Username": order.user.username,
        "Delivery Address": order.delivery_address,
        "Status": order.status,
        "Created At": order.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "Items": "; ".join(
            [f"{item.product.title} (x{item.quantity})" for item in order_items]
        ),
        "Total Price": sum(
            [item.price * item.quantity for item in order_items]
        ),
    }

    if not os.path.exists(EXCEL_FILE_PATH):
        wb = Workbook()
        ws = wb.active
        ws.append(list(order_data.keys()))
        wb.save(EXCEL_FILE_PATH)

    # Асинхронное добавление данных в Excel
    # Поскольку openpyxl не поддерживает асинхронность, используем поток для выполнения блокирующих операций
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, append_order_to_excel, order_data)


def append_order_to_excel(order_data):
    wb = openpyxl.load_workbook(EXCEL_FILE_PATH)
    ws = wb.active
    ws.append(list(order_data.values()))
    wb.save(EXCEL_FILE_PATH)
