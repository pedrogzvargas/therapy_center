from modules.backoffice.user.domain import UserRepository
from modules.backoffice.user.domain import UserAlreadyExist
from modules.backoffice.user.application.create import UserCreator
from modules.backoffice.user.infrastructure.repositories.postgres import PostgresUserRepository
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.environ.domain import Environ
from modules.shared.logger.domain import Logger
from modules.shared.bus.event.domain import EventBus
from modules.shared.password_hasher.domain import PasswordHasher
from modules.shared.environ.infraestructure import PyEnviron
from modules.shared.bus.event.infraestructure.fake import FakeEventBus
from modules.shared.password_hasher.infraestructure import Argon2PasswordHasher
from modules.shared.logger.infraestructure import PyLogger


class UserCreatorController:
    """
    Class controller to create User
    """

    def __init__(
        self,
        user_repository: UserRepository = None,
        password_hasher: PasswordHasher = None,
        event_bus: EventBus = None,
        environ: Environ = None,
        logger: Logger = None,
    ):
        """
        Args:
            user_repository: repository for user database table operations
            password_hasher: password to hash password
            event_bus: event bus
            environ: environ variable reader
            logger: logger
        """

        self.__environ = environ or PyEnviron()
        self.__user_repository = user_repository or PostgresUserRepository(environ=self.__environ)
        self.__password_hasher = password_hasher or Argon2PasswordHasher()
        self.__event_bus = event_bus or FakeEventBus()
        self.__logger = logger or PyLogger(
            level=self.__environ.get_str("LOG_LEVEL"),
            format=self.__environ.get_str("LOG_FORMAT"),
        )

    def __call__(self, body):
        try:
            user_creator = UserCreator(
                user_repository=self.__user_repository,
                password_hasher=self.__password_hasher,
                event_bus=self.__event_bus,
            )
            user_creator(
                user_id=body.get("id"),
                username=body.get("username"),
                password=body.get("password"),
                is_active=body.get("is_active"),
            )
            response = {"success": True, "message": messages.SUCCESS_MESSAGE, "data": {}}, status.HTTP_201_CREATED

        except UserAlreadyExist as ex:
            response = {"success": False, "message": f"{ex}", "data": {}}, status.HTTP_409_CONFLICT
            return response

        except Exception as ex:
            self.__logger.error(f"UserCreatorController: {ex}")
            response = {
                "success": False,
                "message": messages.INTERNAL_SERVER_ERROR,
                "data": {}}, status.HTTP_500_INTERNAL_SERVER_ERROR
            return response

        else:
            return response
