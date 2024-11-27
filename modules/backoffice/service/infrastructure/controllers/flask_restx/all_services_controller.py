from modules.backoffice.service.domain import ServiceRepository
from modules.backoffice.service.application.all import AllServices
from modules.backoffice.service.infrastructure.repositories.postgres import PostgresServiceRepository
from modules.backoffice.service.infrastructure.schemas.marshmallow import ServiceSchema
from modules.shared.serializer.domain import EntitySerializer
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.environ.domain import Environ
from modules.shared.environ.infraestructure import PyEnviron
from modules.shared.serializer.infraestructure.marshmallow import MarshmallowEntitySerializer


class AllServicesController:
    """
    Class controller to get all Services
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

    def __call__(self):
        try:
            all_services = AllServices(service_repository=self.__service_repository)
            all_services = all_services()
            services = self.__entity_serializer(all_services, many=True)
            response = {"success": True, "message": "OK", "data": services}, status.HTTP_200_OK

        except Exception as ex:
            response = {
                "success": False,
                "message": messages.INTERNAL_SERVER_ERROR,
                "data": {}
            }, status.HTTP_500_INTERNAL_SERVER_ERROR
            return response

        else:
            return response
