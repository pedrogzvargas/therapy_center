from uuid import UUID
from modules.shared.persistence.domain import UnitOfWork
from modules.backoffice.product.domain import ProductRepository
from modules.backoffice.product.domain import ProductFinder as DomainProductFinder


class ProductDeleter:
    """
    Class to delete Service
    """

    def __init__(self, unit_of_work: UnitOfWork, product_repository: ProductRepository):
        """
        Args:
            product_repository: repository for product database table operations
        """

        self.__product_repository = product_repository
        self.__unit_of_work = unit_of_work

    async def delete(self, product_id: UUID):
        product_finder = DomainProductFinder(product_repository=self.__product_repository)
        product = await product_finder.find(product_id=product_id)

        async with self.__unit_of_work:
            await self.__product_repository.delete(product.id)
