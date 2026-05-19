from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from modules.backoffice.employee.domain import EmployeeRepository
from modules.backoffice.employee.domain import EmployeeDoesNotExist
from modules.backoffice.employee.application import EmployeeFinder
from modules.backoffice.employee.infrastructure.repositories import PostgresEmployeeRepository
from modules.backoffice.employee.infrastructure.schemas.marshmallow import EmployeeSchema
from modules.shared.serializer.domain import EntitySerializer
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.environ.domain import Environ
from modules.shared.environ.infrastructure import PyEnviron
from modules.shared.serializer.infrastructure.marshmallow import MarshmallowEntitySerializer


class EmployeeFinderController:
    """
    Class controller to get Employee
    """

    def __init__(
        self,
        session: AsyncSession,
        employee_repository: EmployeeRepository | None = None,
        entity_serializer: EntitySerializer | None = None,
        environ: Environ | None = None
    ):
        """
        Args:
            employee_repository: repository for employee database table operations
            entity_serializer: serializer class
            environ: environ variable reader
        """

        self.__session = session
        self.__environ = environ or PyEnviron()
        self.__employee_repository = employee_repository or PostgresEmployeeRepository(session=self.__session)
        self.__entity_serializer = entity_serializer or MarshmallowEntitySerializer(schema=EmployeeSchema())

    async def find(self, employee_id: UUID):
        try:
            employee_finder = EmployeeFinder(employee_repository=self.__employee_repository)
            employee = await employee_finder.find(employee_id=employee_id)
            employee = self.__entity_serializer(employee)
            response = {
                "success": True,
                "message": messages.SUCCESS_MESSAGE,
                "data": employee
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
