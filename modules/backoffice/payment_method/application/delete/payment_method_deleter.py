from uuid import UUID
from modules.backoffice.payment_method.domain import PaymentMethodRepository
from modules.backoffice.payment_method.domain import PaymentMethodFinder as DomainPaymentMethodFinder


class PaymentMethodDeleter:
    """
    Class to delete Payment method
    """

    def __init__(self, payment_method_repository: PaymentMethodRepository):
        """
        Args:
            payment_method_repository: repository for payment method database table operations
        """
        self.__payment_method_repository = payment_method_repository

    def __call__(self, payment_method_id: UUID):
        payment_method_finder = DomainPaymentMethodFinder(payment_method_repository=self.__payment_method_repository)
        payment_method = payment_method_finder(payment_method_id=payment_method_id)
        self.__payment_method_repository.delete(payment_method)
