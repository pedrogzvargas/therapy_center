from uuid import UUID
from modules.backoffice.payment_method.domain import PaymentMethodRepository
from modules.backoffice.payment_method.domain import PaymentMethodFinder
from modules.shared.bus.event.domain import EventBus


class PaymentMethodPatcher:
    """
    Class to patch Payment method
    """

    def __init__(
        self,
        payment_method_repository: PaymentMethodRepository = None,
        event_bus: EventBus = None,
    ):
        """
        Args:
            payment_method_repository: repository for payment method database table operations
            event_bus: event bus to publish event
        """

        self.__payment_method_repository = payment_method_repository
        self.__event_bus = event_bus

    def __call__(self, payment_method_id: UUID, data: dict):
        payment_method_finder = PaymentMethodFinder(payment_method_repository=self.__payment_method_repository)
        payment_method = payment_method_finder(payment_method_id=payment_method_id)
        payment_method.patch(data=data)
        self.__payment_method_repository.save(payment_method=payment_method)
        self.__event_bus.publish(payment_method.pull_domain_events())
