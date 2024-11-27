from uuid import UUID
from abc import ABC
from abc import abstractmethod


class CustomerRepository(ABC):
    """
    Repository for customer database table operations
    """

    @abstractmethod
    def add(self, customer):
        """add customer to session"""
        pass

    @abstractmethod
    def search(self, specifications: list, page: int = 1, page_size: int = 10):
        """search customers"""
        pass

    @abstractmethod
    def all(self):
        """list all customers"""
        pass

    @abstractmethod
    def get(self, id: UUID):
        """get customer"""
        pass

    @abstractmethod
    def save(self, customer):
        """save customer"""
        pass

    @abstractmethod
    def delete(self, customer):
        """delete customer"""
        pass
