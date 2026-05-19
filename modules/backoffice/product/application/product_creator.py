from uuid import UUID
from decimal import Decimal
from modules.shared.persistence.domain import UnitOfWork
from modules.backoffice.product.domain import ProductRepository
from modules.backoffice.product.domain import Product
from modules.backoffice.product.domain import ProductAlreadyExist
from modules.shared.bus.event.domain import EventBus


class ProductCreator:
    """
    Class to create Service
    """

    def __init__(
        self,
        unit_of_work: UnitOfWork,
        service_repository: ProductRepository,
        event_bus: EventBus,
    ):
        """
        Args:
            service_repository: repository for product database table operations
            event_bus: event bus to publish event
        """

        self.__service_repository = service_repository
        self.__unit_of_work = unit_of_work
        self.__event_bus = event_bus

    async def create(self, service_id: UUID, name: str, price: Decimal, is_active: bool, description: str = None):
        if await self.__service_repository.get(id=service_id):
            raise ProductAlreadyExist(f"Service with id: {service_id} already exist")

        async with self.__unit_of_work:
            product = Product.create(id=service_id, name=name, description=description, price=price, is_active=is_active)
            await self.__service_repository.add(product=product)

        self.__event_bus.publish(product.pull_domain_events())
