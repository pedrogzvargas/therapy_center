from uuid import UUID
from modules.backoffice.user.domain import UserRepository
from modules.backoffice.user.domain import User
from modules.backoffice.user.domain import UserAlreadyExist
from modules.shared.password_hasher.domain import PasswordHasher
from modules.shared.bus.event.domain import EventBus


class UserCreator:
    """
    Class to create User
    """

    def __init__(
        self,
        user_repository: UserRepository = None,
        password_hasher: PasswordHasher = None,
        event_bus: EventBus = None,
    ):
        """
        Args:
            user_repository: repository for user database table operations
            password_hasher: password to hash password
            event_bus: event bus to publish event
        """

        self.__user_repository = user_repository
        self.__password_hasher = password_hasher
        self.__event_bus = event_bus

    def __call__(
        self,
        user_id: UUID,
        username: str,
        password: str,
        is_active: bool,
    ):

        if self.__user_repository.get(id=user_id):
            raise UserAlreadyExist(f"User with id: {user_id} already exist")

        user = User.create(
            id=user_id,
            username=username,
            password=self.__password_hasher.hash(password),
            is_active=is_active,
        )

        self.__user_repository.save(user=user)
        self.__event_bus.publish(user.pull_domain_events())
