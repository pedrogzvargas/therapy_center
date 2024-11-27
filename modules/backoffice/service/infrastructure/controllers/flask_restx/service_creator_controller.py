from modules.backoffice.service.domain import ServiceRepository
from modules.backoffice.service.domain import ServiceAlreadyExist
from modules.backoffice.service.application.create import ServiceCreator
from modules.backoffice.service.infrastructure.repositories.postgres import PostgresServiceRepository
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.environ.domain import Environ
from modules.shared.bus.event.domain import EventBus
from modules.shared.environ.infraestructure import PyEnviron
from modules.shared.bus.event.infraestructure.fake import FakeEventBus


class ServiceCreatorController:
    """
    Class controller to create Service
    """

    def __init__(
        self,
        service_repository: ServiceRepository = None,
        event_bus: EventBus = None,
        environ: Environ = None
    ):
        """
        Args:
            service_repository: repository for service database table operations
            environ: environ variable reader
        """

        self.__environ = environ or PyEnviron()
        self.__service_repository = service_repository or PostgresServiceRepository(environ=self.__environ)
        self.__event_bus = event_bus or FakeEventBus()

    def __call__(self, body):
        try:
            service_creator = ServiceCreator(
                service_repository=self.__service_repository,
                event_bus=self.__event_bus,
            )
            service_creator(
                service_id=body.get("id"),
                name=body.get("name"),
                description=body.get("description"),
                price=body.get("price"),
                is_active=body.get("is_active"),
            )
            response = {"success": True, "message": messages.SUCCESS_MESSAGE, "data": {}}, status.HTTP_201_CREATED

        except ServiceAlreadyExist as ex:
            response = {"success": False, "message": f"{ex}", "data": {}}, status.HTTP_409_CONFLICT
            return response

        except Exception as ex:
            response = {"success": False, "message": messages.INTERNAL_SERVER_ERROR, "data": {}}, status.HTTP_500_INTERNAL_SERVER_ERROR
            return response

        else:
            return response
