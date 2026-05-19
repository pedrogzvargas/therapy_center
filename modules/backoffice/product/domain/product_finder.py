from uuid import UUID
from .product_repository import ProductRepository
from .product_does_not_exist import ProductDoesNotExist


class ProductFinder:
    """
    Class to get Product
    """

    def __init__(self, product_repository: ProductRepository):
        """
        Args:
            product_repository: repository for product database table operations
        """
        self.__product_repository = product_repository

    async def find(self, product_id: UUID):
        product = await self.__product_repository.get(id=product_id)

        if not product:
            raise ProductDoesNotExist(f"Product with id: {product_id} does not exist")

        return product
