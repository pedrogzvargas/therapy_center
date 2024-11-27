from uuid import UUID
from .customer_repository import CustomerRepository
from .customer_does_not_exist import CustomerDoesNotExist


class CustomerFinder:
    """
    Class to get Customer
    """

    def __init__(self, customer_repository: CustomerRepository):
        """
        Args:
            customer_repository: repository for customer database table operations
        """
        self.__customer_repository = customer_repository

    def __call__(self, customer_id: UUID):
        customer = self.__customer_repository.get(id=customer_id)

        if not customer:
            raise CustomerDoesNotExist(f"Customer with id: {customer_id} does not exist")

        return customer
