from sqlalchemy.ext.asyncio import AsyncSession
from modules.shared.persistence.domain import UnitOfWork
from modules.backoffice.user.domain import UserRepository
from modules.backoffice.user.domain import UserAlreadyExist
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.bus.event.domain import EventBus
from modules.shared.environ.domain import Environ
from modules.shared.password_hasher.domain import PasswordHasher
from modules.backoffice.customer.domain import CustomerRepository
from modules.shared.persistence.domain import UniqueConstraintError
from modules.backoffice.customer.application import CustomerCreator
from modules.shared.environ.infrastructure import PyEnviron
from modules.shared.persistence.infrastructure import AlchemyUnitOfWork
from modules.shared.bus.event.infrastructure import KafkaEventBus
from modules.backoffice.user.infrastructure.repositories import PostgresUserRepository
from modules.backoffice.customer.infrastructure.repositories import PostgresCustomerRepository
from modules.shared.password_hasher.infrastructure import Argon2PasswordHasher


class CustomerCreatorController:
    """
    Class controller to create Customer
    """

    def __init__(
        self,
        session: AsyncSession,
        environ: Environ | None = None,
        unit_of_work: UnitOfWork | None = None,
        user_repository: UserRepository | None = None,
        customer_repository: CustomerRepository | None = None,
        password_hasher: PasswordHasher | None = None,
        event_bus: EventBus | None = None,
    ):
        """
        Args:
            user_repository: repository for user database table operations
            customer_repository: repository for customer database table operations
            password_hasher: password to hash password
        """

        self.__session = session
        self.__environ = environ or PyEnviron()
        self.__unit_of_work = unit_of_work or AlchemyUnitOfWork(session=self.__session)
        self.__user_repository = user_repository or PostgresUserRepository(session=self.__session)
        self.__customer_repository = customer_repository or PostgresCustomerRepository(session=self.__session)
        self.__password_hasher = password_hasher or Argon2PasswordHasher()
        self.__event_bus = event_bus or KafkaEventBus("localhost:9092")

    async def create(self, body: dict):
        try:
            customer_creator = CustomerCreator(
                unit_of_work=self.__unit_of_work,
                user_repository=self.__user_repository,
                customer_repository=self.__customer_repository,
                password_hasher=self.__password_hasher,
                event_bus=self.__event_bus,
            )
            await customer_creator.create(
                id=body.get("id"),
                name=body.get("name"),
                last_name=body.get("last_name"),
                second_last_name=body.get("second_last_name"),
                email=body.get("email"),
                password=body.get("password"),
                is_active=body.get("is_active"),
            )
            response = {"success": True, "message": messages.SUCCESS_MESSAGE, "data": {}}, status.HTTP_201_CREATED

        except (UserAlreadyExist, UniqueConstraintError) as ex:
            response = {"success": False, "message": f"{ex}", "data": {}}, status.HTTP_409_CONFLICT
            return response

        except Exception as ex:
            response = {"success": False, "message": messages.INTERNAL_SERVER_ERROR, "data": {}}, status.HTTP_500_INTERNAL_SERVER_ERROR
            return response

        else:
            return response
