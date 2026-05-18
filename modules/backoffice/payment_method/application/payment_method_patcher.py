from uuid import UUID
from modules.shared.persistence.domain import UnitOfWork
from modules.backoffice.payment_method.domain import PaymentMethodRepository
from modules.backoffice.payment_method.domain import PaymentMethodFinder
from modules.shared.bus.event.domain import EventBus


class PaymentMethodPatcher:
    """
    Class to patch Payment method
    """

    def __init__(
        self,
        unit_of_work: UnitOfWork,
        payment_method_repository: PaymentMethodRepository,
        event_bus: EventBus,
    ):
        """
        Args:
            payment_method_repository: repository for payment method database table operations
            event_bus: event bus to publish event
        """

        self.__payment_method_repository = payment_method_repository
        self.__unit_of_work = unit_of_work
        self.__event_bus = event_bus

    async def patch(self, payment_method_id: UUID, data: dict):
        payment_method_finder = PaymentMethodFinder(payment_method_repository=self.__payment_method_repository)
        payment_method = await payment_method_finder.find(payment_method_id=payment_method_id)
        payment_method.patch(data=data)

        async with self.__unit_of_work:
            await self.__payment_method_repository.patch(payment_method=payment_method)

        self.__event_bus.publish(payment_method.pull_domain_events())
