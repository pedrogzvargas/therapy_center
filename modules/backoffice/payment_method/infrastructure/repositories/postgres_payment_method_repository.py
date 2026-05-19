from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import String
from sqlalchemy import desc
from sqlalchemy import func
from sqlalchemy import select

from modules.backoffice.payment_method.domain import PaymentMethodRepository
from sqlalchemy_models import PaymentMethodModel
from .payment_method_mapper import PaymentMethodMapper


class PostgresPaymentMethodRepository(PaymentMethodRepository):
    """
    PostgresPaymentMethodRepository
    """

    def __init__(self, session: AsyncSession):
        self.__session = session

    def all(self):
        """list all payment methods"""

        results = self.__session.query(PaymentMethodModel).all()
        results = [PaymentMethodMapper.to_domain(result) for result in results]
        return results

    async def simple_search(self, filters: dict, limit: int = 10, page: int = 1, list_all: bool = False):
        """simple search for customer"""

        stmt = select(PaymentMethodModel).order_by(desc(PaymentMethodModel.created_at))

        # filters
        for field, value in filters.items():
            if hasattr(PaymentMethodModel, field):
                column = getattr(PaymentMethodModel, field)

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

        results = [PaymentMethodMapper.to_domain(result) for result in results]

        return {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": pages,
            "results": results,
        }

    async def get(self, id: UUID):
        """get payment method"""

        payment_method = await self.__session.get(PaymentMethodModel, id)

        if payment_method:
            return PaymentMethodMapper.to_domain(payment_method)

        return None

    async def add(self, payment_method):
        """save payment method"""

        self.__session.add(PaymentMethodMapper.to_model(payment_method))
        await self.__session.flush()

    async def patch(self, payment_method):
        """patch payment method"""

        await self.__session.merge(PaymentMethodMapper.to_model(payment_method))

    async def delete(self, id: UUID):
        """delete payment method"""

        payment_method = await self.__session.get(PaymentMethodModel, id)

        if payment_method:
            await self.__session.delete(payment_method)
            await self.__session.flush()
