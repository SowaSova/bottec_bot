from models.products import Product
from sqlalchemy import func, select


class ProductRepository:
    def __init__(self, session):
        self.session = session
        self.model = Product

    async def get_products(self, category_id: int):
        stmt = (
            select(self.model)
            .filter_by(category_id=category_id)
            .where(self.model.is_available)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_product_by_id(self, product_id: int):
        stmt = select(self.model).where(self.model.id == product_id)
        result = await self.session.execute(stmt)
        product = result.scalars().first()
        return product

    async def count_products(self, category_id: int):
        stmt = (
            select(func.count())
            .select_from(self.model)
            .filter_by(category_id=category_id)
            .where(self.model.is_available)
        )
        result = await self.session.execute(stmt)
        return result.scalar()
