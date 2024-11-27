from uuid import UUID
from dataclasses import dataclass


@dataclass
class PaymentMethod:
    """
    Payment Method entity
    """
    id: UUID
    name: str
    is_active: bool
