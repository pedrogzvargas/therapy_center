from modules.shared.aggregate_root.domain import AggregateRoot
from .service_created_domain_event import ServiceCreatedDomainEvent
from .service_patched_domain_event import ServicePatchedDomainEvent


class Service(AggregateRoot):
    """
    Service entity
    """

    def __init__(self, id, name, price, is_active, description=None):
        self._id = id
        self._name = name
        self._description = description
        self._price = price
        self._is_active = is_active

    @staticmethod
    def create(id, name, price, is_active, description=None):
        service = Service(
            id=id,
            name=name,
            description=description,
            price=price,
            is_active=is_active,
        )

        service.record(
            ServiceCreatedDomainEvent(
                aggregate_id=id,
                name=name,
                description=description,
                price=price,
                is_active=is_active,
            )
        )

        return service

    def patch(self, data: dict):
        for attr, value in data.items():
            if hasattr(self, attr):
                setattr(self, attr, value)

        self.record(
            ServicePatchedDomainEvent(
                aggregate_id=self.id,
                data=data,
            )
        )

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, price):
        self._price = price

    @property
    def is_active(self):
        return self._is_active

    @is_active.setter
    def is_active(self, is_active):
        self._is_active = is_active
