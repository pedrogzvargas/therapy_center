from abc import ABC
from abc import abstractmethod


class Specification(ABC):

    @abstractmethod
    def is_satisfied_by(self, entity):
        """function to serialize entity"""
        pass

    @abstractmethod
    def apply(self, query):
        """function to serialize entity"""
        pass
