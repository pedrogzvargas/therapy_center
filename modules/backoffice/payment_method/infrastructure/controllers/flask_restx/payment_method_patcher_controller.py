from modules.backoffice.payment_method.domain import PaymentMethodRepository
from modules.backoffice.payment_method.application.patch import PaymentMethodPatcher
from modules.backoffice.payment_method.infrastructure.repositories.postgres import PostgresPaymentMethodRepository
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.environ.domain import Environ
from modules.shared.bus.event.domain import EventBus
from modules.shared.environ.infraestructure import PyEnviron
from modules.shared.bus.event.infraestructure.fake import FakeEventBus


class PaymentMethodPatcherController:
    """
    Class controller to patch Payment Method
    """

    def __init__(
        self,
        payment_method_repository: PaymentMethodRepository = None,
        event_bus: EventBus = None,
        environ: Environ = None
    ):
        """
        Args:
            payment_method_repository: repository for payment method database table operations
            environ: environ variable reader
        """

        self.__environ = environ or PyEnviron()
        self.__payment_method_repository = payment_method_repository or PostgresPaymentMethodRepository(
            environ=self.__environ,
        )
        self.__event_bus = event_bus or FakeEventBus()

    def __call__(self, payment_method_id, data):
        try:
            payment_method_patcher = PaymentMethodPatcher(
                payment_method_repository=self.__payment_method_repository,
                event_bus=self.__event_bus,
            )
            payment_method_patcher(
                payment_method_id=payment_method_id,
                data=data,
            )

            response = {"success": True, "message": messages.SUCCESS_MESSAGE, "data": {}}, status.HTTP_200_OK

        except Exception as ex:
            response = {"success": False, "message": messages.INTERNAL_SERVER_ERROR, "data": {}}, status.HTTP_500_INTERNAL_SERVER_ERROR
            return response

        else:
            return response
