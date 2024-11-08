from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update
from keyboards.subscriptions import get_subscription_keyboard
from redis.asyncio import Redis
from services.subscriptions import SubscriptionService


class SubscriptionMiddleware(BaseMiddleware):
    def __init__(self, redis_client: Redis):
        super().__init__()
        self.redis = redis_client

    async def __call__(self, handler, event: TelegramObject, data: dict):
        print("SubscriptionMiddleware started")
        data["redis"] = self.redis
        bot = data["bot"]
        session = data["session"]

        if isinstance(event, Update):
            message = event.message or event.edited_message
            if message:
                telegram_id = str(message.from_user.id)

                subscription_service = SubscriptionService(session, self.redis)
                not_subscribed_chats = (
                    await subscription_service.check_subscriptions(
                        telegram_id, bot
                    )
                )
                if not_subscribed_chats:
                    for chat in not_subscribed_chats:
                        if "invite_link" not in chat or not chat["invite_link"]:
                            chat["invite_link"] = (
                                await subscription_service.get_chat_invite_link(
                                    bot, chat
                                )
                            )
                    keyboard = get_subscription_keyboard(not_subscribed_chats)

                    text = "Пожалуйста, подпишитесь на следующие каналы и группы, чтобы продолжить:"
                    await message.answer(text, reply_markup=keyboard)
                    return
        else:
            print(
                f"SubscriptionMiddleware: Received event of type {type(event)}"
            )

        return await handler(event, data)
