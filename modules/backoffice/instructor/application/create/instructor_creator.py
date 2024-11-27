from uuid import UUID
from modules.backoffice.user.domain import UserRepository
from modules.backoffice.user.domain import User
from modules.backoffice.user.domain import UserAlreadyExist
from modules.backoffice.instructor.domain import InstructorRepository
from modules.backoffice.instructor.domain import Instructor
from modules.backoffice.instructor.domain import InstructorAlreadyExist
from modules.shared.password_hasher.domain import PasswordHasher
from modules.shared.bus.event.domain import EventBus


class InstructorCreator:
    """
    Class to create Instructor
    """

    def __init__(
        self,
        user_repository: UserRepository = None,
        instructor_repository: InstructorRepository = None,
        password_hasher: PasswordHasher = None,
        event_bus: EventBus = None,
    ):
        """
        Args:
            user_repository: repository for user database table operations
            instructor_repository: repository for instructor database table operations
            password_hasher: password to hash password
            event_bus: event bus to publish event
        """

        self.__user_repository = user_repository
        self.__instructor_repository = instructor_repository
        self.__password_hasher = password_hasher
        self.__event_bus = event_bus

    def __call__(
        self,
        id: UUID,
        name: str,
        last_name: str,
        username: str,
        password: str,
        is_active: bool,
        second_last_name: str = None,
    ):

        if self.__user_repository.get(id=id):
            raise UserAlreadyExist(f"User with id: {id} already exist")

        if self.__instructor_repository.get(id=id):
            raise InstructorAlreadyExist(f"User with id: {id} already exist")

        user = User.create(
            id=id,
            username=username,
            password=self.__password_hasher.hash(password),
            is_active=is_active,
        )

        instructor = Instructor.create(
            id=id,
            user_id=user.id,
            name=name,
            last_name=last_name,
            second_last_name=second_last_name,
        )

        self.__user_repository.add(user=user)
        self.__instructor_repository.save(instructor=instructor)
        self.__event_bus.publish(user.pull_domain_events())
        self.__event_bus.publish(instructor.pull_domain_events())
