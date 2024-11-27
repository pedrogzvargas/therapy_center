from modules.backoffice.customer.domain import CustomerRepository
from modules.backoffice.customer.infrastructure.specifications import SpecificationsBuilder


class SearchCustomers:
    """
    Class to get search Customers
    """

    def __init__(self, customer_repository: CustomerRepository):
        """
        Args:
            customer_repository: repository for customer database table operations
        """
        self.__customer_repository = customer_repository

    def __call__(self, query_params: dict, page: int, page_size: int):
        specifications = SpecificationsBuilder.build(query_params)
        return self.__customer_repository.search(specifications, page_size=page_size, page=page)
