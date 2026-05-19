from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import String
from sqlalchemy import desc
from sqlalchemy import func
from sqlalchemy import select

from modules.backoffice.employee.domain import EmployeeRepository
from sqlalchemy_models import EmployeeModel
from .employee_mapper import EmployeeMapper


class PostgresEmployeeRepository(EmployeeRepository):
    """
    PostgresEmployeeRepository
    """

    def __init__(self, session: AsyncSession):
        self.__session = session

    async def add(self, employee):
        """add employee to session"""
        self.__session.add(EmployeeMapper.to_model(employee))
        await self.__session.flush()

    def all(self):
        """list all employees"""

        result = self.__session.query(EmployeeModel).all()
        return result

    async def simple_search(self, filters: dict, limit: int = 10, page: int = 1, list_all: bool = False):
        """simple search for employee"""

        stmt = select(EmployeeModel).order_by(desc(EmployeeModel.created_at))

        # filters
        for field, value in filters.items():
            if hasattr(EmployeeModel, field):
                column = getattr(EmployeeModel, field)

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

        results = [EmployeeMapper.to_domain(result) for result in results]

        return {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": pages,
            "results": results,
        }

    async def get(self, id: UUID):
        """get employee"""

        employee = await self.__session.get(EmployeeModel, id)

        if employee:
            return EmployeeMapper.to_domain(employee)

        return None

    async def delete(self, id: UUID):
        """delete employee"""

        employee = await self.__session.get(EmployeeModel, id)

        if employee:
            await self.__session.delete(employee)
            await self.__session.flush()
