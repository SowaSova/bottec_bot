from aiogram.filters.state import State, StatesGroup


class CartStates(StatesGroup):
    WaitingForQuantity = State()
    WaitingForConfirmation = State()
    WaitingForDeliveryAddress = State()
