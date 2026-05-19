from uuid import UUID
from modules.backoffice.payment_method.domain import PaymentMethodRepository
from modules.backoffice.payment_method.domain import PaymentMethodFinder as DomainPaymentMethodFinder


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

    async def find(self, payment_method_id: UUID):

        payment_method_finder = DomainPaymentMethodFinder(payment_method_repository=self.__payment_method_repository)
        payment_method = await payment_method_finder.find(payment_method_id=payment_method_id)

        return payment_method
