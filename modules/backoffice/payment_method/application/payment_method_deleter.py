from uuid import UUID
from modules.shared.persistence.domain import UnitOfWork
from modules.backoffice.payment_method.domain import PaymentMethodRepository
from modules.backoffice.payment_method.domain import PaymentMethodFinder as DomainPaymentMethodFinder


class PaymentMethodDeleter:
    """
    Class to delete Payment method
    """

    def __init__(self, unit_of_work: UnitOfWork, payment_method_repository: PaymentMethodRepository):
        """
        Args:
            payment_method_repository: repository for payment method database table operations
        """
        self.__payment_method_repository = payment_method_repository
        self.__unit_of_work = unit_of_work

    async def delete(self, payment_method_id: UUID):
        payment_method_finder = DomainPaymentMethodFinder(payment_method_repository=self.__payment_method_repository)
        payment_method = await payment_method_finder.find(payment_method_id=payment_method_id)

        async with self.__unit_of_work:
            await self.__payment_method_repository.delete(payment_method.id)
