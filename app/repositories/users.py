from models.users import TelegramUser
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class UserRepository:
    def __init__(self, session):
        self.session = session
        self.model = TelegramUser

    async def get_users(self):
        stmt = select(self.model)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_or_create_user(self, telegram_id: str, username: str = None):
        result = await self.session.execute(
            select(self.model).filter_by(telegram_id=telegram_id)
        )
        user = result.scalar_one_or_none()
        if user:
            return user
        user = self.model(telegram_id=telegram_id, username=username)
        self.session.add(user)
        await self.session.commit()
        return user

    async def get_user_by_telegram_id(self, telegram_id: str):
        stmt = select(self.model).filter_by(telegram_id=telegram_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    @classmethod
    async def update_subscription_status(
        cls,
        session: AsyncSession,
        telegram_id: str,
        is_subscribed_group: bool,
        is_subscribed_channel: bool,
    ):
        result = await session.execute(
            select(cls.model).filter_by(telegram_id=telegram_id)
        )
        user = result.scalar_one()
        user.is_subscribed_group = is_subscribed_group
        user.is_subscribed_channel = is_subscribed_channel
        await session.commit()
        return user
