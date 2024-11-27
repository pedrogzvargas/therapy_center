from uuid import UUID
from abc import ABC
from abc import abstractmethod


class UserRepository(ABC):
    """
    Repository for user database table operations
    """

    @abstractmethod
    def add(self, user):
        """add user to session"""
        pass

    @abstractmethod
    def all(self):
        """list all users"""
        pass

    @abstractmethod
    def get(self, id: UUID):
        """get user"""
        pass

    @abstractmethod
    def save(self, user):
        """save user"""
        pass

    @abstractmethod
    def delete(self, user):
        """delete user"""
        pass

    @abstractmethod
    def soft_delete(self, user):
        """soft delete user"""
        pass
