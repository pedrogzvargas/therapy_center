from uuid import UUID
from modules.shared.persistence.domain import UnitOfWork
from modules.backoffice.user.domain import UserRepository
from modules.backoffice.user.domain import User
from modules.backoffice.user.domain import UserAlreadyExist
from modules.backoffice.employee.domain import EmployeeRepository
from modules.backoffice.employee.domain import Employee
from modules.backoffice.employee.domain import EmployeeAlreadyExist
from modules.shared.password_hasher.domain import PasswordHasher
from modules.shared.bus.event.domain import EventBus


class EmployeeCreator:
    """
    Class to create Employee
    """

    def __init__(
        self,
        unit_of_work: UnitOfWork,
        user_repository: UserRepository,
        employee_repository: EmployeeRepository,
        password_hasher: PasswordHasher,
        event_bus: EventBus,
    ):
        """
        Args:
            user_repository: repository for user database table operations
            employee_repository: repository for employee database table operations
            password_hasher: password to hash password
            event_bus: event bus to publish event
        """

        self.__user_repository = user_repository
        self.__employee_repository = employee_repository
        self.__password_hasher = password_hasher
        self.__unit_of_work = unit_of_work
        self.__event_bus = event_bus

    async def create(
        self,
        id: UUID,
        name: str,
        last_name: str,
        email: str,
        password: str,
        is_active: bool,
        second_last_name: str | None  = None,
    ):

        if await self.__user_repository.get(id=id):
            raise UserAlreadyExist(f"User with id: {id} already exist")

        if await self.__employee_repository.get(id=id):
            raise EmployeeAlreadyExist(f"User with id: {id} already exist")

        user = User.create(
            id=id,
            email=email,
            password=self.__password_hasher.hash(password),
            is_active=is_active,
        )

        employee = Employee.create(
            id=id,
            user_id=user.id,
            name=name,
            last_name=last_name,
            second_last_name=second_last_name,
        )

        async with self.__unit_of_work:
            await self.__user_repository.add(user=user)
            await self.__employee_repository.add(employee=employee)

        self.__event_bus.publish(user.pull_domain_events())
        self.__event_bus.publish(employee.pull_domain_events())
