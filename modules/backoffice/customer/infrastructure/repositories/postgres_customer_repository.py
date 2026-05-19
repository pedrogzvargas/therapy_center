from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import String
from sqlalchemy import desc
from sqlalchemy import func
from sqlalchemy import select
from modules.backoffice.customer.domain import CustomerRepository
from sqlalchemy_models import CustomerModel
from .customer_mapper import CustomerMapper


class PostgresCustomerRepository(CustomerRepository):
    """
    PostgresCustomerRepository
    """

    def __init__(self, session: AsyncSession):
        self.__session = session

    async def add(self, customer):
        """add customer to session"""

        self.__session.add(CustomerMapper.to_model(customer))
        await self.__session.flush()

    async def simple_search(self, filters: dict, limit: int = 10, page: int = 1, list_all: bool = False):
        """simple search for customer"""

        stmt = select(CustomerModel).order_by(desc(CustomerModel.created_at))

        # filters
        for field, value in filters.items():
            if hasattr(CustomerModel, field):
                column = getattr(CustomerModel, field)

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

        results = [CustomerMapper.to_domain(result) for result in results]

        return {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": pages,
            "results": results,
        }

    def all(self):
        """list all customers"""

        result = self.__session.query(CustomerModel).all()
        return result

    async def get(self, id: UUID):
        """get customer"""

        customer = await self.__session.get(CustomerModel, id)

        if customer:
            return CustomerMapper.to_domain(customer)

        return None

    async def delete(self, id: UUID):
        """delete customer"""

        customer = await self.__session.get(CustomerModel, id)

        if customer:
            await self.__session.delete(customer)
            await self.__session.flush()
