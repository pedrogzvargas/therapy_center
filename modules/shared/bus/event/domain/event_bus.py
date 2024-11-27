from abc import ABC
from abc import abstractmethod


class EventBus(ABC):
    """
    Port to event bus creator
    """

    @abstractmethod
    def publish(self, domain_events):
        """function to publish domain events"""
        pass
