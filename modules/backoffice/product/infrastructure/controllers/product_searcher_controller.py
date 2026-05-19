from sqlalchemy.ext.asyncio import AsyncSession
from modules.backoffice.product.domain import ProductRepository
from modules.backoffice.product.application import ProductSearcher
from modules.backoffice.product.infrastructure.repositories import PostgresProductRepository
from modules.backoffice.product.infrastructure.schemas.marshmallow import SearchProductSchema
from modules.shared.serializer.domain import EntitySerializer
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.environ.domain import Environ
from modules.shared.logger.domain import Logger
from modules.shared.environ.infrastructure import PyEnviron
from modules.shared.serializer.infrastructure.marshmallow import MarshmallowEntitySerializer
from modules.shared.logger.infrastructure import PyLogger


class ProductSearcherController:
    """
    Class controller to search products
    """

    def __init__(
        self,
        session: AsyncSession,
        product_repository: ProductRepository | None = None,
        entity_serializer: EntitySerializer | None = None,
        environ: Environ | None = None,
        logger: Logger | None = None,
    ):
        """
        Args:
            product_repository: repository for customer database table operations
            entity_serializer: serializer class
            environ: environ variable reader
            logger: logger
        """

        self.__environ = environ or PyEnviron()
        self.__session = session
        self.__product_repository = product_repository or PostgresProductRepository(session=self.__session)
        self.__entity_serializer = entity_serializer or MarshmallowEntitySerializer(schema=SearchProductSchema())
        self.__logger = logger or PyLogger(
            level=self.__environ.get_str("LOG_LEVEL"),
            format=self.__environ.get_str("LOG_FORMAT"),
        )

    async def search(self, query_params: dict):
        try:
            product_searcher = ProductSearcher(product_repository=self.__product_repository)
            products = await product_searcher.search(query_params=query_params)
            products = self.__entity_serializer(products)
            response = products, status.HTTP_200_OK

        except Exception as ex:
            self.__logger.error(f"ProductSearcherController: {ex}")
            response = {
                "success": False,
                "message": messages.INTERNAL_SERVER_ERROR,
                "data": {}
            }, status.HTTP_500_INTERNAL_SERVER_ERROR
            return response

        else:
            return response
