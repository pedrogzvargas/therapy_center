from uuid import UUID
from modules.backoffice.product.domain import ProductRepository
from modules.backoffice.product.domain import ProductFinder as DomainProductFinder


class ProductFinder:
    """
    Class to get Service
    """

    def __init__(self, product_repository: ProductRepository):
        """
        Args:
            product_repository: repository for product database table operations
        """

        self.__product_repository = product_repository

    def __call__(self, product_id: UUID):
        return self.find(product_id)

    async def find(self, product_id: UUID):

        product_finder = DomainProductFinder(product_repository=self.__product_repository)
        product = await product_finder.find(product_id=product_id)

        return product
