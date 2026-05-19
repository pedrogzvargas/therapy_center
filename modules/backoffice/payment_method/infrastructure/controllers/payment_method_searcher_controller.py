from sqlalchemy.ext.asyncio import AsyncSession
from modules.backoffice.payment_method.domain import PaymentMethodRepository
from modules.backoffice.payment_method.application import PaymentMethodSearcher
from modules.backoffice.payment_method.infrastructure.repositories import PostgresPaymentMethodRepository
from modules.backoffice.payment_method.infrastructure.schemas.marshmallow import SearchPaymentMethodSchema
from modules.shared.serializer.domain import EntitySerializer
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.environ.domain import Environ
from modules.shared.logger.domain import Logger
from modules.shared.environ.infrastructure import PyEnviron
from modules.shared.serializer.infrastructure.marshmallow import MarshmallowEntitySerializer
from modules.shared.logger.infrastructure import PyLogger


class PaymentMethodSearcherController:
    """
    Class controller to search payment methods
    """

    def __init__(
        self,
        session: AsyncSession,
        payment_method_repository: PaymentMethodRepository | None = None,
        entity_serializer: EntitySerializer | None = None,
        environ: Environ | None = None,
        logger: Logger | None = None,
    ):
        """
        Args:
            payment_method_repository: repository for payment method database table operations
            entity_serializer: serializer class
            environ: environ variable reader
            logger: logger
        """

        self.__environ = environ or PyEnviron()
        self.__session = session
        self.__payment_method_repository = payment_method_repository or PostgresPaymentMethodRepository(session=self.__session)
        self.__entity_serializer = entity_serializer or MarshmallowEntitySerializer(schema=SearchPaymentMethodSchema())
        self.__logger = logger or PyLogger(
            level=self.__environ.get_str("LOG_LEVEL"),
            format=self.__environ.get_str("LOG_FORMAT"),
        )

    async def search(self, query_params: dict):
        try:
            payment_method_searcher = PaymentMethodSearcher(payment_method_repository=self.__payment_method_repository)
            payment_methods = await payment_method_searcher.search(query_params=query_params)
            payment_methods = self.__entity_serializer(payment_methods)
            response = payment_methods, status.HTTP_200_OK

        except Exception as ex:
            self.__logger.error(f"PaymentMethodSearcherController: {ex}")
            response = {
                "success": False,
                "message": messages.INTERNAL_SERVER_ERROR,
                "data": {}
            }, status.HTTP_500_INTERNAL_SERVER_ERROR
            return response

        else:
            return response
