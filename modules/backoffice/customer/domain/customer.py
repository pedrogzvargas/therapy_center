from modules.shared.aggregate_root.domain import AggregateRoot
from .customer_created_domain_event import CustomerCreatedDomainEvent
from .customer_patched_domain_event import CustomerPatchedDomainEvent


class Customer(AggregateRoot):
    """
    Customer entity
    """

    def __init__(self, id, user_id, name, last_name, second_last_name=None):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.last_name = last_name
        self.second_last_name = second_last_name

    @staticmethod
    def create(id, user_id, name, last_name, second_last_name=None):
        customer = Customer(
            id=id,
            user_id=user_id,
            name=name,
            last_name=last_name,
            second_last_name=second_last_name,
        )

        customer.record(
            CustomerCreatedDomainEvent(
                aggregate_id=id,
                user_id=user_id,
                name=name,
                last_name=last_name,
                second_last_name=second_last_name,
            )
        )

        return customer

    def patch(self, data: dict):
        for attr, value in data.items():
            if hasattr(self, attr):
                setattr(self, attr, value)

        self.record(
            CustomerPatchedDomainEvent(
                aggregate_id=self.id,
                data=data,
            )
        )

    def to_dict(self):
        return dict(
            id=self.id,
            user_id=self.user_id,
            name=self.name,
            last_name=self.last_name,
            second_last_name=self.second_last_name,
        )
