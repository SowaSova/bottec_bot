import json

from redis.asyncio import Redis
from services.chats import RequiredChatService
from services.users import UserService


class SubscriptionService:
    def __init__(self, session, redis_client: Redis):
        self.session = session
        self.redis = redis_client
        self.user_service = UserService(session)
        self.chat_service = RequiredChatService(session)

    async def check_subscriptions(self, telegram_id: str, bot):
        cache_key = f"user:{telegram_id}:subscriptions"
        cached_data = await self.redis.get(cache_key)
        if cached_data:
            not_subscribed_chats = json.loads(cached_data)
            return not_subscribed_chats

        required_chats = await self.chat_service.get_required_chats()
        not_subscribed_chats = []

        for chat in required_chats:
            is_member = await self.is_member_of_chat(
                telegram_id, chat.chat_id, bot
            )
            if not is_member:
                not_subscribed_chats.append(
                    {
                        "chat_id": chat.chat_id,
                        "name": chat.title,
                        "username": getattr(chat, "username", None),
                        "chat_type": chat.type,
                    }
                )

        await self.redis.set(
            cache_key,
            json.dumps(not_subscribed_chats),
            ex=1,  # Время жизни кэша в секундах
        )

        return not_subscribed_chats

    async def is_member_of_chat(self, user_id: str, chat_id: str, bot):
        """Проверяет, является ли пользователь членом чата. Работает только если бот установлен в качестве администратора чата."""
        try:
            member = await bot.get_chat_member(chat_id, user_id)
            return member.status != "left"
        except Exception:
            return False

    async def get_chat_invite_link(self, bot, chat):
        if chat.get("username"):
            if chat["username"].startswith("https://t.me/"):
                username = chat["username"].split("/")[-1]
                return f"tg://resolve?domain={username}"
            elif chat["username"].startswith("@"):
                return f"tg://resolve?domain={chat['username'][1:]}"
            else:
                return f"tg://resolve?domain={chat['username']}"
        else:
            try:
                # Создаём пригласительную ссылку и извлекаем хэш
                invite_link = await bot.create_chat_invite_link(chat["chat_id"])
                invite_hash = invite_link.invite_link.split("/")[-1]
                return f"tg://join?invite={invite_hash}"
            except Exception as e:
                print(f"Error creating invite link: {e}")
                return "#"
