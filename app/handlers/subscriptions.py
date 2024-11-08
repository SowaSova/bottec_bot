import datetime
import logging

from aiogram import Bot, F, Router
from aiogram.types import CallbackQuery
from keyboards.subscriptions import get_subscription_keyboard
from services.subscriptions import SubscriptionService

router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(F.data == "check_subscription")
async def process_check_subscription(
    callback_query: CallbackQuery, bot: Bot, session, redis
):
    """
    Обработчик для проверки подписок пользователя на каналы и группы.
    """
    try:
        telegram_id = str(callback_query.from_user.id)

        subscription_service = SubscriptionService(session, redis)
        not_subscribed_chats = await subscription_service.check_subscriptions(
            telegram_id, bot
        )

        if not_subscribed_chats:
            # Получаем ссылки-приглашения для каждого чата, если они еще не получены
            for chat in not_subscribed_chats:
                if "invite_link" not in chat or not chat["invite_link"]:
                    chat["invite_link"] = (
                        await subscription_service.get_chat_invite_link(
                            bot, chat
                        )
                    )

            # Создаем клавиатуру с кнопками чатов и кнопкой "Проверить подписку"
            keyboard = get_subscription_keyboard(not_subscribed_chats)

            # Добавляем временную метку
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            text = (
                f"Вы всё ещё не подписаны на следующие каналы и группы:\n"
                f"(Последнее обновление: {timestamp})"
            )

            await callback_query.message.edit_text(text, reply_markup=keyboard)
            logger.info(
                f"User {callback_query.from_user.id} has {len(not_subscribed_chats)} unsubscribed chats."
            )
        else:
            # Если пользователь подписался на все каналы
            await callback_query.message.edit_text(
                "Спасибо, что подписались! Можете продолжить использование бота."
            )
            logger.info(
                f"User {callback_query.from_user.id} has completed subscriptions."
            )

        await callback_query.answer()
    except Exception as e:
        logger.error(f"Error in process_check_subscription: {e}")
        await callback_query.message.reply(
            "Произошла ошибка при проверке подписок."
        )
        await callback_query.answer()
