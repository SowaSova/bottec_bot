from models.chats import RequiredChat
from sqlalchemy.future import select


class RequiredChatRepository:
    def __init__(self, session):
        self.session = session
        self.model = RequiredChat

    async def get_chats(self):
        result = await self.session.execute(select(self.model))
        return result.scalars().all()
