from models.categories import Category
from sqlalchemy import select


class CategoryRepository:
    def __init__(self, session):
        self.session = session
        self.model = Category

    async def get_root_categories(self):
        stmt = select(self.model).filter_by(parent_id=None)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_subcategories(self, category_id):
        stmt = select(self.model).filter_by(parent_id=category_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()
