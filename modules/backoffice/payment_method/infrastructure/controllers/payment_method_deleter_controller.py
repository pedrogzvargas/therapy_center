from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from modules.shared.persistence.domain import UnitOfWork
from modules.backoffice.payment_method.domain import PaymentMethodRepository
from modules.backoffice.payment_method.domain import PaymentMethodDoesNotExist
from modules.backoffice.payment_method.application import PaymentMethodDeleter
from modules.backoffice.payment_method.infrastructure.repositories import PostgresPaymentMethodRepository
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.environ.domain import Environ
from modules.shared.environ.infrastructure import PyEnviron
from modules.shared.persistence.infrastructure import AlchemyUnitOfWork


class PaymentMethodDeleterController:
    """
    Class controller to delete Payment Method
    """

    def __init__(
        self,
        session: AsyncSession,
        payment_method_repository: PaymentMethodRepository | None = None,
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

    def __call__(self, payment_method_id: UUID):
        return self.delete(payment_method_id)

    async def delete(self, payment_method_id: UUID):
        try:
            payment_method_deleter = PaymentMethodDeleter(
                unit_of_work=self.__unit_of_work,
                payment_method_repository=self.__payment_method_repository,
            )
            await payment_method_deleter.delete(payment_method_id=payment_method_id)
            response = {
                "success": True,
                "message": messages.SUCCESS_MESSAGE,
                "data": {}
            }, status.HTTP_200_OK

        except PaymentMethodDoesNotExist as ex:
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
