from modules.shared.bus.event.domain import DomainEvent


class PaymentMethodCreatedDomainEvent(DomainEvent):

    def __init__(self, aggregate_id, name, is_active, event_id=None, occurred_on=None):
        super().__init__(aggregate_id=aggregate_id, event_id=event_id, occurred_on=occurred_on)
        self.__name = name
        self.__is_active = is_active

    def event_name(self):
        return "backoffice.payment_method.created"

    def to_primitives(self):
        return dict(
            aggregate_id=self.__aggregate_id,
            name=self.__name,
            is_active=self.__is_active,
            event_id=self.__event_id,
            occurred_on=self.__occurred_on,
        )

    def from_primitives(self, aggregate_id, body, event_id, occurred_on):
        return PaymentMethodCreatedDomainEvent(
            aggregate_id=aggregate_id,
            name=body.get("name"),
            is_active=body.get("is_active"),
            event_id=event_id,
            occurred_on=occurred_on,
        )

    @property
    def name(self):
        return self.__name

    @property
    def is_active(self):
        return self.__is_active
