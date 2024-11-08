from repositories.users import UserRepository


class UserService:
    def __init__(self, session):
        self.session = session
        self.repository = UserRepository(session)

    async def get_users(self):
        return await self.repository.get_users()

    async def register_user(self, telegram_id: str, username: str = None):
        user = await self.repository.get_or_create_user(telegram_id, username)
        return user

    async def check_subscriptions(self, telegram_id: str, bot):
        is_subscribed_group = await self.is_member_of_chat(
            telegram_id, "group_chat_id", bot
        )
        is_subscribed_channel = await self.is_member_of_chat(
            telegram_id, "channel_chat_id", bot
        )
        await self.repository.update_subscription_status(
            telegram_id, is_subscribed_group, is_subscribed_channel
        )

    async def get_user_id_by_telegram_id(self, tg_user_id: str):
        user = await self.repository.get_user_by_telegram_id(
            telegram_id=tg_user_id
        )
        return user.id

    async def is_member_of_chat(self, user_id: str, chat_id: str, bot):
        try:
            member = await bot.get_chat_member(chat_id, user_id)
            return member.status != "left"
        except Exception:
            return False
