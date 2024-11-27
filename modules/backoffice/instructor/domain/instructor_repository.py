from uuid import UUID
from abc import ABC
from abc import abstractmethod


class InstructorRepository(ABC):
    """
    Repository for instructor database table operations
    """

    @abstractmethod
    def add(self, instructor):
        """add instructor to session"""
        pass

    @abstractmethod
    def all(self):
        """list all instructors"""
        pass

    @abstractmethod
    def get(self, id: UUID):
        """get instructor"""
        pass

    @abstractmethod
    def save(self, instructor):
        """save instructor"""
        pass

    @abstractmethod
    def delete(self, instructor):
        """delete instructor"""
        pass
