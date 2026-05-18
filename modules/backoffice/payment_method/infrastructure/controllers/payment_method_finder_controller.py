from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from modules.shared.persistence.domain import UnitOfWork
from modules.backoffice.payment_method.domain import PaymentMethodRepository
from modules.backoffice.payment_method.domain import PaymentMethodDoesNotExist
from modules.backoffice.payment_method.application import PaymentMethodFinder
from modules.backoffice.payment_method.infrastructure.repositories import PostgresPaymentMethodRepository
from modules.backoffice.payment_method.infrastructure.schemas.marshmallow import PaymentMethodSchema
from modules.shared.serializer.domain import EntitySerializer
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.environ.domain import Environ
from modules.shared.environ.infrastructure import PyEnviron
from modules.shared.logger.domain import Logger
from modules.shared.serializer.infrastructure.marshmallow import MarshmallowEntitySerializer
from modules.shared.persistence.infrastructure import AlchemyUnitOfWork
from modules.shared.logger.infrastructure import PyLogger


class PaymentMethodFinderController:
    """
    Class controller to get Payment Method
    """

    def __init__(
        self,
        session: AsyncSession,
        payment_method_repository: PaymentMethodRepository | None = None,
        entity_serializer: EntitySerializer | None = None,
        environ: Environ | None = None,
        unit_of_work: UnitOfWork | None = None,
        logger: Logger | None = None,
    ):
        """
        Args:
            payment_method_repository: repository for payment method database table operations
            entity_serializer: serializer class
            environ: environ variable reader
        """

        self.__environ = environ or PyEnviron()
        self.__session = session
        self.__unit_of_work = unit_of_work or AlchemyUnitOfWork(session=self.__session)
        self.__payment_method_repository = payment_method_repository or PostgresPaymentMethodRepository(
            session=self.__session,
        )
        self.__entity_serializer = entity_serializer or MarshmallowEntitySerializer(schema=PaymentMethodSchema())
        self.__logger = logger or PyLogger(
            level=self.__environ.get_str("LOG_LEVEL"),
            format=self.__environ.get_str("LOG_FORMAT"),
        )

    async def find(self, payment_method_id: UUID):
        try:
            payment_method_finder = PaymentMethodFinder(
                payment_method_repository=self.__payment_method_repository,
            )
            payment_method = await payment_method_finder.find(payment_method_id=payment_method_id)
            payment_methods = self.__entity_serializer(payment_method)
            response = {
                "success": True,
                "message": messages.SUCCESS_MESSAGE,
                "data": payment_methods
            }, status.HTTP_200_OK

        except PaymentMethodDoesNotExist as ex:
            response = {"success": False, "message": f"{ex}", "data": {}}, status.HTTP_404_NOT_FOUND
            return response

        except Exception as ex:
            self.__logger.error(f"PaymentMethodFinderController: {ex}")
            response = {
                "success": False,
                "message": messages.INTERNAL_SERVER_ERROR,
                "data": {}
            }, status.HTTP_500_INTERNAL_SERVER_ERROR
            return response

        else:
            return response
