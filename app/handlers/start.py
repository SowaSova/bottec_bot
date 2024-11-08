import logging

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from keyboards.start import get_main_keyboard
from services.users import UserService

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command(commands=["start"]))
async def start_command(message: types.Message, state: FSMContext, session):
    """
    Обработчик команды /start. Регистрирует пользователя и отправляет главное меню.
    """
    try:
        user_service = UserService(session)
        await user_service.register_user(
            str(message.chat.id), message.from_user.username
        )
        kb = get_main_keyboard()

        await message.answer("Добро пожаловать!", reply_markup=kb)
        logger.info(f"Пользователь {message.from_user.id} запустил бота.")
    except Exception as e:
        logger.error(f"Ошибка при выполнении команды /start: {e}")
        await message.reply("Произошла ошибка при запуске бота.")
