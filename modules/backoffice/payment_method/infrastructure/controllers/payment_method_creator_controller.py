from sqlalchemy.ext.asyncio import AsyncSession
from modules.shared.persistence.domain import UnitOfWork
from modules.backoffice.payment_method.domain import PaymentMethodRepository
from modules.backoffice.payment_method.domain import PaymentMethodAlreadyExist
from modules.backoffice.payment_method.application import PaymentMethodCreator
from modules.backoffice.payment_method.infrastructure.repositories import PostgresPaymentMethodRepository
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.environ.domain import Environ
from modules.shared.bus.event.domain import EventBus
from modules.shared.environ.infrastructure import PyEnviron
from modules.shared.bus.event.infrastructure import FakeEventBus
from modules.shared.persistence.infrastructure import AlchemyUnitOfWork


class PaymentMethodCreatorController:
    """
    Class controller to create Payment Method
    """

    def __init__(
        self,
        session: AsyncSession,
        payment_method_repository: PaymentMethodRepository | None = None,
        event_bus: EventBus | None = None,
        environ: Environ | None = None,
        unit_of_work: UnitOfWork | None = None,
    ):
        """
        Args:
            payment_method_repository: repository for payment method database table operations
            environ: environ variable reader
        """

        self.__environ = environ or PyEnviron()
        self.__session = session
        self.__unit_of_work = unit_of_work or AlchemyUnitOfWork(session=self.__session)
        self.__payment_method_repository = payment_method_repository or PostgresPaymentMethodRepository(
            session=self.__session,
        )
        self.__event_bus = event_bus or FakeEventBus()

    async def create(self, body):
        try:
            payment_method_creator = PaymentMethodCreator(
                unit_of_work=self.__unit_of_work,
                payment_method_repository=self.__payment_method_repository,
                event_bus=self.__event_bus,
            )
            await payment_method_creator.create(
                payment_method_id=body.get("id"),
                name=body.get("name"),
                is_active=body.get("is_active"),
            )
            response = {"success": True, "message": messages.SUCCESS_MESSAGE, "data": {}}, status.HTTP_201_CREATED

        except PaymentMethodAlreadyExist as ex:
            response = {"success": False, "message": f"{ex}", "data": {}}, status.HTTP_409_CONFLICT
            return response

        except Exception as ex:
            response = {
                "success": False,
                "message": messages.INTERNAL_SERVER_ERROR,
                "data": {},
            }, status.HTTP_500_INTERNAL_SERVER_ERROR
            return response

        else:
            return response
