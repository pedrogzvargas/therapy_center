from modules.shared.aggregate_root.domain import AggregateRoot
from .payment_method_created_domain_event import PaymentMethodCreatedDomainEvent
from .payment_method_patched_domain_event import PaymentMethodPatchedDomainEvent


class PaymentMethod(AggregateRoot):
    """
    Payment Method entity
    """

    def __init__(self, id, name, is_active, created_at, updated_at):
        super().__init__()
        self.id = id
        self.name = name
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def create(id, name, is_active, created_at=None, updated_at=None):
        payment_method = PaymentMethod(
            id=id,
            name=name,
            is_active=is_active,
            created_at=created_at,
            updated_at=updated_at,
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
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
