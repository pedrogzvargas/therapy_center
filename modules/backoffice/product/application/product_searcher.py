from modules.backoffice.product.domain import ProductRepository


class ProductSearcher:
    """
    Class to get search products
    """

    def __init__(self, product_repository: ProductRepository):
        """
        Args:
            product_repository: repository for customer database table operations
        """

        self.__product_repository = product_repository

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

        product_results = await self.__product_repository.simple_search(
            filters=cleaned_query_params,
            limit=limit,
            page=page,
            list_all=export,
        )

        return product_results
