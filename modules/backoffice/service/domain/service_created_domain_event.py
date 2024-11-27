from modules.shared.bus.event.domain import DomainEvent


class ServiceCreatedDomainEvent(DomainEvent):

    def __init__(
        self,
        aggregate_id,
        name,
        description,
        price,
        is_active,
        event_id=None,
        occurred_on=None,
    ):
        super().__init__(aggregate_id=aggregate_id, event_id=event_id, occurred_on=occurred_on)
        self.__name = name
        self.__description = description
        self.__price = price
        self.__is_active = is_active

    def event_name(self):
        return "backoffice.service.created"

    def to_primitives(self):
        return dict(
            aggregate_id=self.__aggregate_id,
            name=self.__name,
            description=self.__description,
            price=self.__price,
            is_active=self.__is_active,
            event_id=self.__event_id,
            occurred_on=self.__occurred_on,
        )

    def from_primitives(self, aggregate_id, body, event_id, occurred_on):
        return ServiceCreatedDomainEvent(
            aggregate_id=aggregate_id,
            name=body.get("name"),
            description=body.get("description"),
            price=body.get("price"),
            is_active=body.get("is_active"),
            event_id=event_id,
            occurred_on=occurred_on,
        )

    @property
    def name(self):
        return self.__name

    @property
    def description(self):
        return self.__description

    @property
    def price(self):
        return self.__price

    @property
    def is_active(self):
        return self.__is_active
