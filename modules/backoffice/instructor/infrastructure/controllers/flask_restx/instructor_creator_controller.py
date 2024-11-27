from modules.backoffice.user.domain import UserRepository
from modules.backoffice.user.domain import UserAlreadyExist
from modules.backoffice.user.infrastructure.repositories.postgres import PostgresUserRepository
from modules.backoffice.instructor.domain import InstructorRepository
from modules.backoffice.instructor.application.create import InstructorCreator
from modules.backoffice.instructor.infrastructure.repositories.postgres import PostgresInstructorRepository
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.environ.domain import Environ
from modules.shared.bus.event.domain import EventBus
from modules.shared.environ.infraestructure import PyEnviron
from modules.shared.bus.event.infraestructure.fake import FakeEventBus
from modules.shared.password_hasher.domain import PasswordHasher
from modules.shared.password_hasher.infraestructure import Argon2PasswordHasher


class InstructorCreatorController:
    """
    Class controller to create Instructor
    """

    def __init__(
        self,
        user_repository: UserRepository = None,
        instructor_repository: InstructorRepository = None,
        password_hasher: PasswordHasher = None,
        event_bus: EventBus = None,
        environ: Environ = None
    ):
        """
        Args:
            user_repository: repository for user database table operations
            instructor_repository: repository for instructor database table operations
            password_hasher: password to hash password
            environ: environ variable reader
        """

        self.__environ = environ or PyEnviron()
        self.__user_repository = user_repository or PostgresUserRepository(environ=self.__environ)
        self.__instructor_repository = instructor_repository or PostgresInstructorRepository(environ=self.__environ)
        self.__password_hasher = password_hasher or Argon2PasswordHasher()
        self.__event_bus = event_bus or FakeEventBus()

    def __call__(self, body):
        try:
            instructor_creator = InstructorCreator(
                user_repository=self.__user_repository,
                instructor_repository=self.__instructor_repository,
                password_hasher=self.__password_hasher,
                event_bus=self.__event_bus,
            )
            instructor_creator(
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
