from repositories.products import ProductRepository


class ProductService:
    def __init__(self, session):
        self.session = session
        self.repository = ProductRepository(session)

    async def get_products(self, category_id: int):
        return await self.repository.get_products(category_id)

    async def get_product_by_id(self, product_id: int):
        return await self.repository.get_product_by_id(product_id)

    async def count_products(self, category_id: int):
        return await self.repository.count_products(category_id)
