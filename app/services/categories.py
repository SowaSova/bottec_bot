from repositories.categories import CategoryRepository


class CategoryService:
    def __init__(self, session):
        self.session = session
        self.repository = CategoryRepository(session)

    async def get_root_categories(self):
        return await self.repository.get_root_categories()

    async def get_subcategories(self, category_id):
        return await self.repository.get_subcategories(category_id)
