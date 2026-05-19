from modules.backoffice.payment_method.domain import PaymentMethodRepository


class PaymentMethodSearcher:
    """
    Class to get search payment methods
    """

    def __init__(self, payment_method_repository: PaymentMethodRepository):
        """
        Args:
            payment_method_repository: repository for customer database table operations
        """

        self.__payment_method_repository = payment_method_repository

    async def search(self, query_params: dict):
        """
        Args:
            query_params (dict): query params.
        Returns:
            dict: paginated products.
        """

        if not isinstance(query_params, dict):
            raise ValueError(f"query_params: {query_params} is not instance of dict")

        limit = query_params.pop("limit", 10)
        page = query_params.pop("page", 1)
        export = query_params.pop("export", False)

        cleaned_query_params = {key: value for key, value in query_params.items() if value not in [None, ""]}

        payment_methods_results = await self.__payment_method_repository.simple_search(
            filters=cleaned_query_params,
            limit=limit,
            page=page,
            list_all=export,
        )

        return payment_methods_results
