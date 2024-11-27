from modules.app.payment_method.domain import PaymentMethodRepository
from modules.app.payment_method.application.services import AllPaymentMethods
from modules.app.payment_method.infrastructure.repositories.postgres import PostgresPaymentMethodRepository
from modules.app.payment_method.infrastructure.schemas.marshmallow import PaymentMethodSchema
from modules.shared.serializer.domain import EntitySerializer
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.environ.domain import Environ
from modules.shared.environ.infraestructure import PyEnviron
from modules.shared.serializer.infraestructure.marshmallow import MarshmallowEntitySerializer


class AllPaymentMethodsController:
    """
    Class controller to get all Payment Methods
    """

    def __init__(
        self,
        payment_method_repository: PaymentMethodRepository = None,
        entity_serializer: EntitySerializer = None,
        environ: Environ = None
    ):
        """
        Args:
            payment_method_repository: repository for payment method database table operations
            entity_serializer: serializer class
            environ: environ variable reader
        """

        self.__environ = environ or PyEnviron()
        self.__payment_method_repository = payment_method_repository or PostgresPaymentMethodRepository(
            environ=self.__environ,
        )
        self.__entity_serializer = entity_serializer or MarshmallowEntitySerializer(schema=PaymentMethodSchema())

    def __call__(self):
        try:
            all_payment_methods = AllPaymentMethods(payment_method_repository=self.__payment_method_repository)
            all_payment_methods = all_payment_methods()
            payment_methods = self.__entity_serializer(all_payment_methods, many=True)
            response = {"success": True, "message": messages.SUCCESS_MESSAGE, "data": payment_methods}, status.HTTP_200_OK
        except Exception as ex:
            response = {"success": False, "message": messages.INTERNAL_SERVER_ERROR, "data": {}}, status.HTTP_404_NOT_FOUND
            return response

        else:
            return response
