from uuid import UUID
from modules.shared.persistence.domain import UnitOfWork
from modules.backoffice.user.domain import UserRepository
from modules.backoffice.user.domain import UserFinder
from modules.backoffice.employee.domain import EmployeeRepository
from modules.backoffice.employee.domain import EmployeeFinder as DomainEmployeeFinder


class EmployeeDeleter:
    """
    Class to delete Employee
    """

    def __init__(
        self,
        unit_of_work: UnitOfWork,
        user_repository: UserRepository,
        employee_repository: EmployeeRepository
    ):
        """
        Args:
            employee_repository: repository for customer database table operations
        """

        self.__unit_of_work = unit_of_work
        self.__user_repository = user_repository
        self.__employee_repository = employee_repository

    async def delete(self, employee_id: UUID):
        async with self.__unit_of_work:
            employee_finder = DomainEmployeeFinder(employee_repository=self.__employee_repository)
            user_finder = UserFinder(user_repository=self.__user_repository)
            employee = await employee_finder.find(employee_id=employee_id)
            user = await user_finder.find(user_id=employee.user_id)
            await self.__employee_repository.delete(employee.id)
            await self.__user_repository.delete(user.id)
