from modules.shared.aggregate_root.domain import AggregateRoot
from .payment_method_created_domain_event import PaymentMethodCreatedDomainEvent
from .payment_method_patched_domain_event import PaymentMethodPatchedDomainEvent


class PaymentMethod(AggregateRoot):
    """
    Payment Method entity
    """

    def __init__(self, id, name, is_active):
        self.__id = id
        self.__name = name
        self.__is_active = is_active

    @staticmethod
    def create(id, name, is_active):
        payment_method = PaymentMethod(
            id=id,
            name=name,
            is_active=is_active,
        )

        payment_method.record(PaymentMethodCreatedDomainEvent(aggregate_id=id, name=name, is_active=is_active))

        return payment_method

    def patch(self, data: dict):
        for attr, value in data.items():
            if hasattr(self, attr):
                setattr(self, attr, value)

        self.record(
            PaymentMethodPatchedDomainEvent(
                aggregate_id=self.id,
                data=data,
            )
        )

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            is_active=self.is_active,
        )

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def is_active(self):
        return self.__is_active

    @is_active.setter
    def is_active(self, is_active):
        self.__is_active = is_active

