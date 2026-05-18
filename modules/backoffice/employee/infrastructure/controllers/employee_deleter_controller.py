from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from modules.shared.persistence.domain import UnitOfWork
from modules.backoffice.employee.domain import EmployeeRepository
from modules.backoffice.employee.domain import EmployeeDoesNotExist
from modules.backoffice.employee.application import EmployeeDeleter
from modules.backoffice.employee.infrastructure.repositories import PostgresEmployeeRepository
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.environ.domain import Environ
from modules.backoffice.user.domain import UserRepository
from modules.shared.environ.infrastructure import PyEnviron
from modules.shared.persistence.infrastructure import AlchemyUnitOfWork
from modules.backoffice.user.infrastructure.repositories import PostgresUserRepository


class EmployeeDeleterController:
    """
    Class controller to delete Employee
    """

    def __init__(
        self,
        session: AsyncSession,
        employee_repository: EmployeeRepository | None = None,
        user_repository: UserRepository | None = None,
        environ: Environ | None = None,
        unit_of_work: UnitOfWork | None = None,
    ):
        """
        Args:
            employee_repository: repository for employee database table operations
            environ: environ variable reader
        """

        self.__session = session
        self.__environ = environ or PyEnviron()
        self.__unit_of_work = unit_of_work or AlchemyUnitOfWork(session=self.__session)
        self.__employee_repository = employee_repository or PostgresEmployeeRepository(session=self.__session)
        self.__user_repository = user_repository or PostgresUserRepository(session=self.__session)

    async def delete(self, employee_id: UUID):
        try:
            employee_deleter = EmployeeDeleter(
                unit_of_work=self.__unit_of_work,
                user_repository=self.__user_repository,
                employee_repository=self.__employee_repository,
            )
            await employee_deleter.delete(employee_id=employee_id)

            response = {
                "success": True,
                "message": messages.SUCCESS_MESSAGE,
                "data": {}
            }, status.HTTP_200_OK

        except EmployeeDoesNotExist as ex:
            response = {"success": False, "message": f"{ex}", "data": {}}, status.HTTP_404_NOT_FOUND
            return response

        except Exception as ex:
            response = {
                "success": False,
                "message": messages.INTERNAL_SERVER_ERROR,
                "data": {}
            }, status.HTTP_500_INTERNAL_SERVER_ERROR
            return response

        else:
            return response
