from uuid import UUID
from abc import ABC
from abc import abstractmethod


class EmployeeRepository(ABC):
    """
    Repository for employee database table operations
    """

    @abstractmethod
    async def add(self, employee):
        """add employee to session"""
        pass

    @abstractmethod
    async def all(self):
        """list all employees"""
        pass

    @abstractmethod
    async def simple_search(self, filters: dict, limit: int = 10, page: int = 1, list_all: bool = False):
        """simple employee search"""
        pass

    @abstractmethod
    async def get(self, id: UUID):
        """get employee"""
        pass

    @abstractmethod
    async def delete(self, employee):
        """delete employee"""
        pass
