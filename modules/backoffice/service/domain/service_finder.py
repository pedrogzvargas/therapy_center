from uuid import UUID
from .service_repository import ServiceRepository
from .service_does_not_exist import ServiceDoesNotExist


class ServiceFinder:
    """
    Class to get Service
    """

    def __init__(self, service_repository: ServiceRepository):
        """
        Args:
            service_repository: repository for service database table operations
        """
        self.__service_repository = service_repository

    def __call__(self, service_id: UUID):
        service = self.__service_repository.get(id=service_id)

        if not service:
            raise ServiceDoesNotExist(f"Service with id: {service_id} does not exist")

        return service
