from sqlalchemy.ext.asyncio import AsyncSession


class CustomService:
    def __init__(self, session: AsyncSession):
        self.session = session
