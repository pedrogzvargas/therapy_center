from uuid import UUID
from modules.backoffice.service.domain import ServiceRepository
from modules.backoffice.service.domain import ServiceFinder
from modules.shared.bus.event.domain import EventBus


class ServicePatcher:
    """
    Class to patch Service
    """

    def __init__(
        self,
        service_repository: ServiceRepository = None,
        event_bus: EventBus = None,
    ):
        """
        Args:
            service_repository: repository for service database table operations
            event_bus: event bus to publish event
        """

        self.__service_repository = service_repository
        self.__event_bus = event_bus

    def __call__(self, service_id: UUID, data: dict):
        service_finder = ServiceFinder(service_repository=self.__service_repository)
        service = service_finder(service_id=service_id)
        service.patch(data=data)
        self.__service_repository.save(service=service)
        self.__event_bus.publish(service.pull_domain_events())
