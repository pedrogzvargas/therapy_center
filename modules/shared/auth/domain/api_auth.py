from abc import ABC
from abc import abstractmethod


class ApiAuth(ABC):

    @abstractmethod
    def allowed(self):
        """function to check if user is allowed"""
        pass

    @abstractmethod
    def get_user(self):
        """function to get authenticated user"""
        pass
