from uuid import UUID
from modules.backoffice.service.domain import ServiceRepository
from modules.backoffice.service.domain import ServiceDoesNotExist
from modules.backoffice.service.application.delete import ServiceDeleter
from modules.backoffice.service.infrastructure.repositories.postgres import PostgresServiceRepository
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.environ.domain import Environ
from modules.shared.environ.infraestructure import PyEnviron


class ServiceDeleterController:
    """
    Class controller to delete Service
    """

    def __init__(
        self,
        service_repository: ServiceRepository = None,
        environ: Environ = None
    ):
        """
        Args:
            service_repository: repository for Service database table operations
            environ: environ variable reader
        """

        self.__environ = environ or PyEnviron()
        self.__service_repository = service_repository or PostgresServiceRepository(environ=self.__environ)

    def __call__(self, service_id: UUID):
        try:
            service_deleter = ServiceDeleter(service_repository=self.__service_repository)
            service_deleter(service_id=service_id)
            response = {
                "success": True,
                "message": messages.SUCCESS_MESSAGE,
                "data": {}
            }, status.HTTP_200_OK

        except ServiceDoesNotExist as ex:
            response = {"success": False, "message": f"{ex}", "data": {}}, status.HTTP_404_NOT_FOUND
            return response

        except Exception as ex:
            response = {
                "success": False,
                "message": messages.INTERNAL_SERVER_ERROR,
                "data": {}
            }, status.HTTP_500_INTERNAL_SERVER_ERROR
            return response

        else:
            return response
