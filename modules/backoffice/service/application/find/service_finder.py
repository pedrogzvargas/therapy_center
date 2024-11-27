from uuid import UUID
from modules.backoffice.service.domain import ServiceRepository
from modules.backoffice.service.domain import ServiceFinder as DomainServiceFinder


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
        service_finder = DomainServiceFinder(service_repository=self.__service_repository)
        service = service_finder(service_id=service_id)
        return service
