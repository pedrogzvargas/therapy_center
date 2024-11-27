from uuid import UUID
from decimal import Decimal
from modules.backoffice.service.domain import ServiceRepository
from modules.backoffice.service.domain import Service
from modules.backoffice.service.domain import ServiceAlreadyExist
from modules.shared.bus.event.domain import EventBus


class ServiceCreator:
    """
    Class to create Service
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

    def __call__(self, service_id: UUID, name: str, price: Decimal, is_active: bool, description: str = None):
        if self.__service_repository.get(id=service_id):
            raise ServiceAlreadyExist(f"Service with id: {service_id} already exist")
        service = Service.create(id=service_id, name=name, description=description, price=price, is_active=is_active)
        self.__service_repository.save(service=service)
        self.__event_bus.publish(service.pull_domain_events())
