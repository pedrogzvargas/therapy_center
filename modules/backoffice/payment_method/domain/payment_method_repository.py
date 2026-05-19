from uuid import UUID
from abc import ABC
from abc import abstractmethod


class PaymentMethodRepository(ABC):
    """
    Repository for payment method database table operations
    """

    @abstractmethod
    async def all(self):
        """list all payment methods"""
        pass

    @abstractmethod
    async def simple_search(self, filters: dict, limit: int = 10, page: int = 1, list_all: bool = False):
        """simple payment search"""
        pass

    @abstractmethod
    async def get(self, id: UUID):
        """get payment method"""
        pass

    async def add(self, payment_method):
        """add payment method"""
        pass

    async def patch(self, payment_method):
        """patch payment method"""
        pass

    @abstractmethod
    async def delete(self, id: UUID):
        """delete payment method"""
        pass
