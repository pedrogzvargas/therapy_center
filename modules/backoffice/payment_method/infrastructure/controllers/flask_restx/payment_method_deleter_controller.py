from uuid import UUID
from modules.backoffice.payment_method.domain import PaymentMethodRepository
from modules.backoffice.payment_method.domain import PaymentMethodDoesNotExist
from modules.backoffice.payment_method.application.delete import PaymentMethodDeleter
from modules.backoffice.payment_method.infrastructure.repositories.postgres import PostgresPaymentMethodRepository
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.environ.domain import Environ
from modules.shared.environ.infraestructure import PyEnviron


class PaymentMethodDeleterController:
    """
    Class controller to delete Payment Method
    """

    def __init__(
        self,
        payment_method_repository: PaymentMethodRepository = None,
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

    def __call__(self, payment_method_id: UUID):
        try:
            payment_method_deleter = PaymentMethodDeleter(payment_method_repository=self.__payment_method_repository)
            payment_method_deleter(payment_method_id=payment_method_id)
            response = {
                "success": True,
                "message": messages.SUCCESS_MESSAGE,
                "data": {}
            }, status.HTTP_200_OK

        except PaymentMethodDoesNotExist as ex:
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
