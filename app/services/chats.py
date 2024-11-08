from repositories.chats import RequiredChatRepository


class RequiredChatService:
    def __init__(self, session):
        self.session = session
        self.repository = RequiredChatRepository(session)

    async def get_required_chats(self):
        return await self.repository.get_chats()
