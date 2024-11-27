from uuid import UUID
from abc import ABC
from abc import abstractmethod


class ServiceRepository(ABC):
    """
    Repository for service database table operations
    """

    @abstractmethod
    def all(self):
        """list all services"""
        pass

    @abstractmethod
    def get(self, id: UUID):
        """get service"""
        pass

    @abstractmethod
    def save(self, service):
        """save service"""
        pass

    @abstractmethod
    def delete(self, service):
        """delete service"""
        pass
