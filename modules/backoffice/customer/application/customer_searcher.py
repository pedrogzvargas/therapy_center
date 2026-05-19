from modules.backoffice.customer.domain import CustomerRepository


class CustomerSearcher:
    """
    Class to get search Customers
    """

    def __init__(self, customer_repository: CustomerRepository):
        """
        Args:
            customer_repository: repository for customer database table operations
        """

        self.__customer_repository = customer_repository

    async def search(self, query_params: dict):
        """
        Args:
            query_params (dict): query params.
        Returns:
            dict: paginated customers.
        """

        if not isinstance(query_params, dict):
            raise ValueError(f"query_params: {query_params} is not instance of dict")

        limit = query_params.pop("limit", 10)
        page = query_params.pop("page", 1)
        export = query_params.pop("export", False)

        cleaned_query_params = {key: value for key, value in query_params.items() if value not in [None, ""]}

        customer_results = await self.__customer_repository.simple_search(
            filters=cleaned_query_params,
            limit=limit,
            page=page,
            list_all=export,
        )

        return customer_results
