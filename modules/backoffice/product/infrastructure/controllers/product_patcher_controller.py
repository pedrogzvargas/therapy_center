from sqlalchemy.ext.asyncio import AsyncSession
from modules.shared.persistence.domain import UnitOfWork
from modules.backoffice.product.domain import ProductRepository
from modules.backoffice.product.domain import ProductDoesNotExist
from modules.backoffice.product.application import ProductPatcher
from modules.backoffice.product.infrastructure.repositories import PostgresProductRepository
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.environ.domain import Environ
from modules.shared.bus.event.domain import EventBus
from modules.shared.environ.infrastructure import PyEnviron
from modules.shared.bus.event.infrastructure import FakeEventBus
from modules.shared.persistence.infrastructure import AlchemyUnitOfWork


class ProductPatcherController:
    """
    Class controller to patch Product
    """

    def __init__(
        self,
        session: AsyncSession,
        product_repository: ProductRepository | None = None,
        event_bus: EventBus | None = None,
        environ: Environ | None = None,
        unit_of_work: UnitOfWork | None = None,
    ):
        """
        Args:
            product_repository: repository for product database table operations
            environ: environ variable reader
        """

        self.__session = session
        self.__environ = environ or PyEnviron()
        self.__unit_of_work = unit_of_work or AlchemyUnitOfWork(session=self.__session)
        self.__product_repository = product_repository or PostgresProductRepository(session=self.__session)
        self.__event_bus = event_bus or FakeEventBus()

    async def patch(self, product_id, data):
        try:
            product_patcher = ProductPatcher(
                product_repository=self.__product_repository,
                unit_of_work=self.__unit_of_work,
                event_bus=self.__event_bus,
            )

            await product_patcher.patch(
                product_id=product_id,
                data=data,
            )

            response = {"success": True, "message": messages.SUCCESS_MESSAGE, "data": {}}, status.HTTP_200_OK

        except ProductDoesNotExist as ex:
            response = {"success": False, "message": f"{ex}", "data": {}}, status.HTTP_404_NOT_FOUND
            return response

        except Exception as ex:
            response = {"success": False, "message": messages.INTERNAL_SERVER_ERROR, "data": {}}, status.HTTP_500_INTERNAL_SERVER_ERROR
            return response

        else:
            return response
