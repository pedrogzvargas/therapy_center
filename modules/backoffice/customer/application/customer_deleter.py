from uuid import UUID
from modules.shared.persistence.domain import UnitOfWork
from modules.backoffice.user.domain import UserRepository
from modules.backoffice.user.domain import UserFinder
from modules.backoffice.customer.domain import CustomerRepository
from modules.backoffice.customer.domain import CustomerFinder as DomainCustomerFinder


class CustomerDeleter:
    """
    Class to delete Customer
    """

    def __init__(
        self,
        unit_of_work: UnitOfWork,
        user_repository: UserRepository,
        customer_repository: CustomerRepository
    ):
        """
        Args:
            customer_repository: repository for customer database table operations
        """

        self.__unit_of_work = unit_of_work
        self.__user_repository = user_repository
        self.__customer_repository = customer_repository

    async def delete(self, customer_id: UUID):
        async with self.__unit_of_work:
            customer_finder = DomainCustomerFinder(customer_repository=self.__customer_repository)
            user_finder = UserFinder(user_repository=self.__user_repository)
            customer = await customer_finder.find(customer_id=customer_id)
            user = await user_finder.find(user_id=customer.user_id)

            await self.__customer_repository.delete(customer.id)
            await self.__user_repository.delete(user.id)
