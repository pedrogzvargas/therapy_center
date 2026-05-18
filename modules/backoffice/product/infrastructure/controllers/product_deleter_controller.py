from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from modules.shared.persistence.domain import UnitOfWork
from modules.backoffice.product.domain import ProductRepository
from modules.backoffice.product.domain import ProductDoesNotExist
from modules.backoffice.product.application import ProductDeleter
from modules.backoffice.product.infrastructure.repositories import PostgresProductRepository
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.environ.domain import Environ
from modules.shared.environ.infrastructure import PyEnviron
from modules.shared.persistence.infrastructure import AlchemyUnitOfWork


class ProductDeleterController:
    """
    Class controller to delete Service
    """

    def __init__(
        self,
        session: AsyncSession,
        product_repository: ProductRepository | None = None,
        environ: Environ | None = None,
        unit_of_work: UnitOfWork | None = None,
    ):
        """
        Args:
            product_repository: repository for Service database table operations
            environ: environ variable reader
        """

        self.__environ = environ or PyEnviron()
        self.__session = session
        self.__unit_of_work = unit_of_work or AlchemyUnitOfWork(session=self.__session)
        self.__product_repository = product_repository or PostgresProductRepository(session=self.__session)

    async def delete(self, product_id: UUID):
        try:
            product_deleter = ProductDeleter(
                unit_of_work=self.__unit_of_work,
                product_repository=self.__product_repository,
            )
            await product_deleter.delete(product_id=product_id)
            response = {
                "success": True,
                "message": messages.SUCCESS_MESSAGE,
                "data": {}
            }, status.HTTP_200_OK

        except ProductDoesNotExist as ex:
            response = {"success": False, "message": f"{ex}", "data": {}}, status.HTTP_404_NOT_FOUND
            return response

        except Exception as ex:
            response = {
                "success": False,
                "message": messages.INTERNAL_SERVER_ERROR,
                "data": {}
            }, status.HTTP_500_INTERNAL_SERVER_ERROR
            return response

        else:
            return response
