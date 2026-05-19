from uuid import UUID
from .employee_repository import EmployeeRepository
from .employee_does_not_exist import EmployeeDoesNotExist


class EmployeeFinder:
    """
    Class to get Employee
    """

    def __init__(self, employee_repository: EmployeeRepository):
        """
        Args:
            employee_repository: repository for employee database table operations
        """
        self.__employee_repository = employee_repository

    async def find(self, employee_id: UUID):
        employee = await self.__employee_repository.get(id=employee_id)

        if not employee:
            raise EmployeeDoesNotExist(f"Employee with id: {employee_id} does not exist")

        return employee
