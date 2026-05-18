from modules.shared.aggregate_root.domain import AggregateRoot
from .product_created_domain_event import ProductCreatedDomainEvent
from .product_patched_domain_event import ProductPatchedDomainEvent


class Product(AggregateRoot):
    """
    Product entity
    """

    def __init__(self, id, name, price, is_active, created_at=None, updated_at=None, description=None):
        super().__init__()
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def create(id, name, price, is_active, created_at=None, updated_at=None, description=None):
        product = Product(
            id=id,
            name=name,
            description=description,
            price=price,
            is_active=is_active,
            created_at=created_at,
            updated_at=updated_at,
        )

        product.record(
            ProductCreatedDomainEvent(
                aggregate_id=id,
                name=name,
                description=description,
                price=price,
                is_active=is_active,
            )
        )

        return product

    def patch(self, data: dict):
        for attr, value in data.items():
            if hasattr(self, attr):
                setattr(self, attr, value)

        self.record(
            ProductPatchedDomainEvent(
                aggregate_id=self.id,
                data=data,
            )
        )
