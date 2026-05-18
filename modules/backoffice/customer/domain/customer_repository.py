from uuid import UUID
from abc import ABC
from abc import abstractmethod


class CustomerRepository(ABC):
    """
    Repository for customer database table operations
    """

    @abstractmethod
    async def add(self, customer):
        """add customer to session"""
        pass

    @abstractmethod
    async def simple_search(self, filters: dict, limit: int = 10, page: int = 1, list_all: bool = False):
        """simple customer search"""
        pass

    @abstractmethod
    def all(self):
        """list all customers"""
        pass

    @abstractmethod
    async def get(self, id: UUID):
        """get customer"""
        pass

    @abstractmethod
    async def delete(self, id: UUID):
        """delete customer"""
        pass
