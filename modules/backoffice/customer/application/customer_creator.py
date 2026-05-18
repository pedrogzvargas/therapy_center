from uuid import UUID
from modules.shared.persistence.domain import UnitOfWork
from modules.backoffice.user.domain import UserRepository
from modules.backoffice.user.domain import User
from modules.backoffice.user.domain import UserAlreadyExist
from modules.backoffice.customer.domain import CustomerRepository
from modules.backoffice.customer.domain import Customer
from modules.backoffice.customer.domain import CustomerAlreadyExist
from modules.shared.password_hasher.domain import PasswordHasher
from modules.shared.bus.event.domain import EventBus


class CustomerCreator:
    """
    Class to create Customer
    """

    def __init__(
        self,
        unit_of_work: UnitOfWork,
        user_repository: UserRepository,
        customer_repository: CustomerRepository,
        password_hasher: PasswordHasher,
        event_bus: EventBus,
    ):
        """
        Args:
            user_repository: repository for user database table operations
            customer_repository: repository for customer database table operations
            password_hasher: password to hash password
            event_bus: event bus to publish event
        """

        self.__unit_of_work = unit_of_work
        self.__user_repository = user_repository
        self.__customer_repository = customer_repository
        self.__password_hasher = password_hasher
        self.__event_bus = event_bus

    async def create(
        self,
        id: UUID,
        name: str,
        last_name: str,
        username: str,
        password: str,
        is_active: bool,
        second_last_name: str | None = None,
    ):

        if await self.__user_repository.get(id=id):
            raise UserAlreadyExist(f"User with id: {id} already exist")

        if await self.__customer_repository.get(id=id):
            raise CustomerAlreadyExist(f"Customer with id: {id} already exist")

        user = User.create(
            id=id,
            username=username,
            password=self.__password_hasher.hash(password),
            is_active=is_active,
        )

        customer = Customer.create(
            id=id,
            user_id=user.id,
            name=name,
            last_name=last_name,
            second_last_name=second_last_name,
        )

        async with self.__unit_of_work:
            await self.__user_repository.add(user=user)
            await self.__customer_repository.add(customer=customer)

        self.__event_bus.publish(user.pull_domain_events())
        self.__event_bus.publish(customer.pull_domain_events())
