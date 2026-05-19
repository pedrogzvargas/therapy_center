from uuid import UUID
from abc import ABC
from abc import abstractmethod


class UserRepository(ABC):
    """
    Repository for user database table operations
    """

    @abstractmethod
    async def add(self, user):
        """add user to session"""
        pass

    @abstractmethod
    async def all(self):
        """list all users"""
        pass

    @abstractmethod
    async def get(self, id: UUID):
        """get user"""
        pass

    @abstractmethod
    async def delete(self, user):
        """delete user"""
        pass

    @abstractmethod
    async def soft_delete(self, user):
        """soft delete user"""
        pass
