from uuid import UUID
from modules.backoffice.payment_method.domain import PaymentMethodRepository
from modules.backoffice.payment_method.domain import PaymentMethod
from modules.backoffice.payment_method.domain import PaymentMethodAlreadyExist
from modules.shared.bus.event.domain import EventBus


class PaymentMethodCreator:
    """
    Class to create Payment method
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

    def __call__(self, payment_method_id: UUID, name: str, is_active: bool):
        if self.__payment_method_repository.get(id=payment_method_id):
            raise PaymentMethodAlreadyExist(f"Payment method with id: {payment_method_id} already exist")
        payment_method = PaymentMethod.create(id=payment_method_id, name=name, is_active=is_active)
        self.__payment_method_repository.save(payment_method=payment_method)
        self.__event_bus.publish(payment_method.pull_domain_events())
