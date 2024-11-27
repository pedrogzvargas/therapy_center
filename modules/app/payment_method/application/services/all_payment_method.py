from modules.app.payment_method.domain import PaymentMethodRepository


class AllPaymentMethods:
    """
    Class to get all Payment methods
    """

    def __init__(self, payment_method_repository: PaymentMethodRepository):
        """
        Args:
            payment_method_repository: repository for payment method database table operations
        """
        self.__payment_method_repository = payment_method_repository

    def __call__(self):
        return self.__payment_method_repository.all()
