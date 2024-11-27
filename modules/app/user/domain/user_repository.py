from uuid import UUID
from abc import ABC
from abc import abstractmethod


class UserRepository(ABC):
    """
    Repository for user database table operations
    """

    @abstractmethod
    def all(self):
        """list all users"""
        pass

    @abstractmethod
    def get(self, id: UUID):
        """get user"""
        pass

    @abstractmethod
    def get_by_username(self, username: str):  # TODO Refactor to specification
        """get user by username"""
        pass

    @abstractmethod
    def save(self, user):
        """save user"""
        pass

    @abstractmethod
    def delete(self, payment_method):
        """delete user"""
        pass
