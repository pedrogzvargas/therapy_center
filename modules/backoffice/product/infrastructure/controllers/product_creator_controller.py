from sqlalchemy.ext.asyncio import AsyncSession
from modules.shared.persistence.domain import UnitOfWork
from modules.backoffice.product.domain import ProductRepository
from modules.backoffice.product.domain import ProductAlreadyExist
from modules.backoffice.product.application import ProductCreator
from modules.backoffice.product.infrastructure.repositories import PostgresProductRepository
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.environ.domain import Environ
from modules.shared.bus.event.domain import EventBus
from modules.shared.environ.infrastructure import PyEnviron
from modules.shared.bus.event.infrastructure import FakeEventBus
from modules.shared.persistence.infrastructure import AlchemyUnitOfWork


class ProductCreatorController:
    """
    Class controller to create Service
    """

    def __init__(
        self,
        session: AsyncSession,
        service_repository: ProductRepository | None = None,
        event_bus: EventBus | None = None,
        environ: Environ | None = None,
        unit_of_work: UnitOfWork | None = None,
    ):
        """
        Args:
            service_repository: repository for product database table operations
            environ: environ variable reader
        """

        self.__session = session
        self.__environ = environ or PyEnviron()
        self.__unit_of_work = unit_of_work or AlchemyUnitOfWork(session=self.__session)
        self.__service_repository = service_repository or PostgresProductRepository(session=self.__session)
        self.__event_bus = event_bus or FakeEventBus()

    async def create(self, body):
        try:
            product_creator = ProductCreator(
                service_repository=self.__service_repository,
                unit_of_work=self.__unit_of_work,
                event_bus=self.__event_bus,
            )
            await product_creator.create(
                service_id=body.get("id"),
                name=body.get("name"),
                description=body.get("description"),
                price=body.get("price"),
                is_active=body.get("is_active"),
            )
            response = {"success": True, "message": messages.SUCCESS_MESSAGE, "data": {}}, status.HTTP_201_CREATED

        except ProductAlreadyExist as ex:
            response = {"success": False, "message": f"{ex}", "data": {}}, status.HTTP_409_CONFLICT
            return response

        except Exception as ex:
            response = {"success": False, "message": messages.INTERNAL_SERVER_ERROR, "data": {}}, status.HTTP_500_INTERNAL_SERVER_ERROR
            return response

        else:
            return response
