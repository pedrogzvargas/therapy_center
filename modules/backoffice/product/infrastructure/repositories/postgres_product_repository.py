from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import String
from sqlalchemy import desc
from sqlalchemy import func
from sqlalchemy import select

from modules.backoffice.product.domain import ProductRepository
from sqlalchemy_models import ProductModel
from .product_mapper import ProductMapper


class PostgresProductRepository(ProductRepository):
    """
    PostgresProductRepository
    """

    def __init__(self, session: AsyncSession):
        self.__session = session

    def all(self):
        """list all products"""

        results = self.__session.query(ProductModel).all()
        results = [ProductMapper.to_domain(result) for result in results]
        return results

    async def simple_search(self, filters: dict, limit: int = 10, page: int = 1, list_all: bool = False):
        """simple search for customer"""

        stmt = select(ProductModel).order_by(desc(ProductModel.created_at))

        # filters
        for field, value in filters.items():
            if hasattr(ProductModel, field):
                column = getattr(ProductModel, field)

                if isinstance(column.type, String) and isinstance(value, str):
                    stmt = stmt.where(column.ilike(value))
                else:
                    stmt = stmt.where(column == value)

        # count
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = await self.__session.scalar(count_stmt)

        # pagination
        limit = total if list_all else limit
        pages = (total + limit - 1) // limit if total >= 1 else 0

        if total > limit:
            offset = (page - 1) * limit
            stmt = stmt.offset(offset).limit(limit)

        result = await self.__session.execute(stmt)
        results = result.scalars().all()

        results = [ProductMapper.to_domain(result) for result in results]

        return {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": pages,
            "results": results,
        }

    async def get(self, id: UUID):
        """get product"""

        product = await self.__session.get(ProductModel, id)

        if product:
            return ProductMapper.to_domain(product)

        return None

    async def add(self, product):
        """save product"""

        self.__session.add(ProductMapper.to_model(product))
        await self.__session.flush()

    async def patch(self, product):
        """patch product"""

        await self.__session.merge(ProductMapper.to_model(product))

    async def delete(self, id: UUID):
        """delete product"""

        product = await self.__session.get(ProductModel, id)

        if product:
            await self.__session.delete(product)
            await self.__session.flush()
