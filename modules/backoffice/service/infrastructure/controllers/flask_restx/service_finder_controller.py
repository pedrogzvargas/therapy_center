from uuid import UUID
from modules.backoffice.service.domain import ServiceRepository
from modules.backoffice.service.domain import ServiceDoesNotExist
from modules.backoffice.service.application.find import ServiceFinder
from modules.backoffice.service.infrastructure.repositories.postgres import PostgresServiceRepository
from modules.backoffice.service.infrastructure.schemas.marshmallow import ServiceSchema
from modules.shared.serializer.domain import EntitySerializer
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.environ.domain import Environ
from modules.shared.environ.infraestructure import PyEnviron
from modules.shared.serializer.infraestructure.marshmallow import MarshmallowEntitySerializer


class ServiceFinderController:
    """
    Class controller to get Service
    """

    def __init__(
        self,
        service_repository: ServiceRepository = None,
        entity_serializer: EntitySerializer = None,
        environ: Environ = None
    ):
        """
        Args:
            service_repository: repository for service database table operations
            entity_serializer: serializer class
            environ: environ variable reader
        """

        self.__environ = environ or PyEnviron()
        self.__service_repository = service_repository or PostgresServiceRepository(environ=self.__environ)
        self.__entity_serializer = entity_serializer or MarshmallowEntitySerializer(schema=ServiceSchema())

    def __call__(self, service_id: UUID):
        try:
            service_finder = ServiceFinder(service_repository=self.__service_repository)
            service = service_finder(service_id=service_id)
            service = self.__entity_serializer(service)
            response = {
                "success": True,
                "message": messages.SUCCESS_MESSAGE,
                "data": service
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
