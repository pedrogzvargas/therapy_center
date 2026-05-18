from sqlalchemy.ext.asyncio import AsyncSession
from modules.shared.persistence.domain import UnitOfWork
from modules.backoffice.user.domain import UserRepository
from modules.backoffice.user.domain import UserAlreadyExist
from modules.backoffice.user.infrastructure.repositories import PostgresUserRepository
from modules.backoffice.employee.domain import EmployeeRepository
from modules.backoffice.employee.application import EmployeeCreator
from modules.backoffice.employee.infrastructure.repositories import PostgresEmployeeRepository
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.environ.domain import Environ
from modules.shared.bus.event.domain import EventBus
from modules.shared.environ.infrastructure import PyEnviron
from modules.shared.bus.event.infrastructure import FakeEventBus
from modules.shared.password_hasher.domain import PasswordHasher
from modules.shared.persistence.infrastructure import AlchemyUnitOfWork
from modules.shared.password_hasher.infrastructure import Argon2PasswordHasher


class EmployeeCreatorController:
    """
    Class controller to create Employee
    """

    def __init__(
        self,
        session: AsyncSession,
        user_repository: UserRepository | None = None,
        employee_repository: EmployeeRepository | None = None,
        password_hasher: PasswordHasher | None = None,
        unit_of_work: UnitOfWork | None = None,
        event_bus: EventBus | None = None,
        environ: Environ | None = None
    ):
        """
        Args:
            user_repository: repository for user database table operations
            employee_repository: repository for employee database table operations
            password_hasher: password to hash password
            environ: environ variable reader
        """

        self.__session = session
        self.__environ = environ or PyEnviron()
        self.__unit_of_work = unit_of_work or AlchemyUnitOfWork(session=self.__session)
        self.__user_repository = user_repository or PostgresUserRepository(session=self.__session)
        self.__employee_repository = employee_repository or PostgresEmployeeRepository(session=self.__session)
        self.__password_hasher = password_hasher or Argon2PasswordHasher()
        self.__event_bus = event_bus or FakeEventBus()

    async def create(self, body):
        try:
            employee_creator = EmployeeCreator(
                unit_of_work=self.__unit_of_work,
                user_repository=self.__user_repository,
                employee_repository=self.__employee_repository,
                password_hasher=self.__password_hasher,
                event_bus=self.__event_bus,
            )

            await employee_creator.create(
                id=body.get("id"),
                name=body.get("name"),
                last_name=body.get("last_name"),
                second_last_name=body.get("second_last_name"),
                username=body.get("username"),
                password=body.get("password"),
                is_active=body.get("is_active"),
            )
            response = {"success": True, "message": messages.SUCCESS_MESSAGE, "data": {}}, status.HTTP_201_CREATED

        except UserAlreadyExist as ex:
            response = {"success": False, "message": f"{ex}", "data": {}}, status.HTTP_409_CONFLICT
            return response

        except Exception as ex:
            response = {"success": False, "message": messages.INTERNAL_SERVER_ERROR, "data": {}}, status.HTTP_500_INTERNAL_SERVER_ERROR
            return response

        else:
            return response
