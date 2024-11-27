from uuid import UUID
from modules.backoffice.customer.domain import CustomerRepository
from modules.backoffice.customer.domain import CustomerFinder as DomainCustomerFinder


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
        customer_finder = DomainCustomerFinder(customer_repository=self.__customer_repository)
        customer = customer_finder(customer_id=customer_id)
        return customer
