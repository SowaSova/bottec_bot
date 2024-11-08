from models.faq import FAQ
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class FAQRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.model = FAQ

    async def get_faqs(self, query: str):
        stmt = (
            select(self.model)
            .where(self.model.question.ilike(f"%{query}%"))
            .limit(5)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
