from modules.backoffice.service.domain import ServiceRepository


class AllServices:
    """
    Class to get all Services
    """

    def __init__(self, service_repository: ServiceRepository):
        """
        Args:
            service_repository: repository for service database table operations
        """
        self.__service_repository = service_repository

    def __call__(self):
        return self.__service_repository.all()
