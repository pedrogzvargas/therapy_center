from modules.backoffice.customer.domain import CustomerRepository


class AllCustomers:
    """
    Class to get all Customers
    """

    def __init__(self, customer_repository: CustomerRepository):
        """
        Args:
            customer_repository: repository for customer database table operations
        """
        self.__customer_repository = customer_repository

    def __call__(self):
        return self.__customer_repository.all()
