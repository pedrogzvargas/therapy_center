from uuid import UUID
from abc import ABC
from abc import abstractmethod


class ProductRepository(ABC):
    """
    Repository for product database table operations
    """

    @abstractmethod
    def all(self):
        """list all products"""
        pass

    @abstractmethod
    async def simple_search(self, filters: dict, limit: int = 10, page: int = 1, list_all: bool = False):
        """simple product search"""
        pass

    @abstractmethod
    async def get(self, id: UUID):
        """get product"""
        pass

    @abstractmethod
    async def add(self, product):
        """save product"""
        pass

    async def patch(self, product):
        """patch product"""
        pass

    @abstractmethod
    async def delete(self, id: UUID):
        """delete product"""
        pass
