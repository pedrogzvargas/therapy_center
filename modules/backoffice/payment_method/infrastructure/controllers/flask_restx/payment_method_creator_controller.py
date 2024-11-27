from modules.backoffice.payment_method.domain import PaymentMethodRepository
from modules.backoffice.payment_method.domain import PaymentMethodAlreadyExist
from modules.backoffice.payment_method.application.create import PaymentMethodCreator
from modules.backoffice.payment_method.infrastructure.repositories.postgres import PostgresPaymentMethodRepository
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.environ.domain import Environ
from modules.shared.bus.event.domain import EventBus
from modules.shared.environ.infraestructure import PyEnviron
from modules.shared.bus.event.infraestructure.fake import FakeEventBus


class PaymentMethodCreatorController:
    """
    Class controller to create Payment Method
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

    def __call__(self, body):
        try:
            payment_method_creator = PaymentMethodCreator(
                payment_method_repository=self.__payment_method_repository,
                event_bus=self.__event_bus,
            )
            payment_method_creator(
                payment_method_id=body.get("id"),
                name=body.get("name"),
                is_active=body.get("is_active"),
            )
            response = {"success": True, "message": messages.SUCCESS_MESSAGE, "data": {}}, status.HTTP_201_CREATED

        except PaymentMethodAlreadyExist as ex:
            response = {"success": False, "message": f"{ex}", "data": {}}, status.HTTP_409_CONFLICT
            return response

        except Exception as ex:
            response = {"success": False, "message": messages.INTERNAL_SERVER_ERROR, "data": {}}, status.HTTP_500_INTERNAL_SERVER_ERROR
            return response

        else:
            return response
