from uuid import UUID
from abc import ABC
from abc import abstractmethod


class PaymentMethodRepository(ABC):
    """
    Repository for payment method database table operations
    """

    @abstractmethod
    def all(self):
        """list all payment methods"""
        pass

    @abstractmethod
    def get(self, id: UUID):
        """get payment method"""
        pass
