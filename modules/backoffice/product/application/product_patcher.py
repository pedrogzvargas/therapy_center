from uuid import UUID
from modules.shared.persistence.domain import UnitOfWork
from modules.backoffice.product.domain import ProductRepository
from modules.backoffice.product.domain import ProductFinder
from modules.shared.bus.event.domain import EventBus


class ProductPatcher:
    """
    Class to patch Service
    """

    def __init__(
        self,
        unit_of_work: UnitOfWork,
        product_repository: ProductRepository,
        event_bus: EventBus,
    ):
        """
        Args:
            product_repository: repository for product database table operations
            event_bus: event bus to publish event
        """

        self.__product_repository = product_repository
        self.__unit_of_work = unit_of_work
        self.__event_bus = event_bus

    async def patch(self, product_id: UUID, data: dict):
        product_finder = ProductFinder(product_repository=self.__product_repository)
        product = await product_finder.find(product_id=product_id)
        product.patch(data=data)

        async with self.__unit_of_work:
            await self.__product_repository.patch(product=product)

        self.__event_bus.publish(product.pull_domain_events())
