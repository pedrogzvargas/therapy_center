from uuid import UUID
from modules.backoffice.employee.domain import EmployeeRepository
from modules.backoffice.employee.domain import EmployeeFinder as DomainEmployeeFinder


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
        employee_finder = DomainEmployeeFinder(employee_repository=self.__employee_repository)
        employee = await employee_finder.find(employee_id=employee_id)
        return employee
