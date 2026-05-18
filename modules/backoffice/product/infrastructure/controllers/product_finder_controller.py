from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from modules.backoffice.product.domain import ProductRepository
from modules.backoffice.product.domain import ProductDoesNotExist
from modules.backoffice.product.application import ProductFinder
from modules.backoffice.product.infrastructure.repositories import PostgresProductRepository
from modules.backoffice.product.infrastructure.schemas.marshmallow import ProductSchema
from modules.shared.serializer.domain import EntitySerializer
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.environ.domain import Environ
from modules.shared.environ.infrastructure import PyEnviron
from modules.shared.serializer.infrastructure.marshmallow import MarshmallowEntitySerializer


class ProductFinderController:
    """
    Class controller to get Service
    """

    def __init__(
        self,
        session: AsyncSession,
        product_repository: ProductRepository | None = None,
        entity_serializer: EntitySerializer | None = None,
        environ: Environ | None = None,
    ):
        """
        Args:
            product_repository: repository for product database table operations
            entity_serializer: serializer class
            environ: environ variable reader
        """

        self.__environ = environ or PyEnviron()
        self.__session = session
        self.__product_repository = product_repository or PostgresProductRepository(session=self.__session)
        self.__entity_serializer = entity_serializer or MarshmallowEntitySerializer(schema=ProductSchema())

    async def find(self, product_id: UUID):
        try:
            product_finder = ProductFinder(product_repository=self.__product_repository)
            product = await product_finder.find(product_id=product_id)
            product = self.__entity_serializer(product)
            response = {
                "success": True,
                "message": messages.SUCCESS_MESSAGE,
                "data": product
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
