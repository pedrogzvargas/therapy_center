from sqlalchemy.ext.asyncio import AsyncSession
from modules.backoffice.employee.domain import EmployeeRepository
from modules.backoffice.employee.application import EmployeeSearcher
from modules.backoffice.employee.infrastructure.repositories import PostgresEmployeeRepository
from modules.backoffice.employee.infrastructure.schemas.marshmallow import SearchEmployeeSchema
from modules.shared.serializer.domain import EntitySerializer
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.environ.domain import Environ
from modules.shared.logger.domain import Logger
from modules.shared.environ.infrastructure import PyEnviron
from modules.shared.serializer.infrastructure.marshmallow import MarshmallowEntitySerializer
from modules.shared.logger.infrastructure import PyLogger


class EmployeeSearcherController:
    """
    Class controller to search Employees
    """

    def __init__(
        self,
        session: AsyncSession,
        employee_repository: EmployeeRepository | None = None,
        entity_serializer: EntitySerializer | None = None,
        environ: Environ | None = None,
        logger: Logger | None = None,
    ):
        """
        Args:
            employee_repository: repository for employee database table operations
            entity_serializer: serializer class
            environ: environ variable reader
            logger: logger
        """

        self.__environ = environ or PyEnviron()
        self.__session = session
        self.__employee_repository = employee_repository or PostgresEmployeeRepository(session=self.__session)
        self.__entity_serializer = entity_serializer or MarshmallowEntitySerializer(schema=SearchEmployeeSchema())
        self.__logger = logger or PyLogger(
            level=self.__environ.get_str("LOG_LEVEL"),
            format=self.__environ.get_str("LOG_FORMAT"),
        )

    async def search(self, query_params: dict):
        try:
            employee_searcher = EmployeeSearcher(
                employee_repository=self.__employee_repository,
            )
            employees = await employee_searcher.search(query_params=query_params)
            employees = self.__entity_serializer(employees)
            response = employees, status.HTTP_200_OK

        except Exception as ex:
            self.__logger.error(f"EmployeeSearcherController: {ex}")
            response = {
                "success": False,
                "message": messages.INTERNAL_SERVER_ERROR,
                "data": {}
            }, status.HTTP_500_INTERNAL_SERVER_ERROR
            return response

        else:
            return response
