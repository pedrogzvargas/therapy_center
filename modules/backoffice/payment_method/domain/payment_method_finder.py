from uuid import UUID
from .payment_method_repository import PaymentMethodRepository
from .payment_method_does_not_exist import PaymentMethodDoesNotExist


class PaymentMethodFinder:
    """
    Class to get Payment method
    """

    def __init__(self, payment_method_repository: PaymentMethodRepository):
        """
        Args:
            payment_method_repository: repository for payment method database table operations
        """
        self.__payment_method_repository = payment_method_repository

    def __call__(self, payment_method_id: UUID):
        payment_method = self.__payment_method_repository.get(id=payment_method_id)

        if not payment_method:
            raise PaymentMethodDoesNotExist(f"Payment Method with id: {payment_method_id} does not exist")

        return payment_method
