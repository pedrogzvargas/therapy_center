from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from modules.shared.persistence.domain import UnitOfWork
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.environ.domain import Environ
from modules.backoffice.customer.domain import CustomerRepository
from modules.backoffice.customer.domain import CustomerDoesNotExist
from modules.backoffice.user.domain import UserRepository
from modules.backoffice.customer.application import CustomerDeleter
from modules.shared.environ.infrastructure import PyEnviron
from modules.shared.persistence.infrastructure import AlchemyUnitOfWork
from modules.backoffice.customer.infrastructure.repositories import PostgresCustomerRepository
from modules.backoffice.user.infrastructure.repositories import PostgresUserRepository


class CustomerDeleterController:
    """
    Class controller to delete Customer
    """

    def __init__(
        self,
        session: AsyncSession,
        customer_repository: CustomerRepository | None = None,
        user_repository: UserRepository | None = None,
        environ: Environ | None = None,
        unit_of_work: UnitOfWork | None = None,
    ):
        """
        Args:
            customer_repository: repository for customer database table operations
            environ: environ variable reader
        """

        self.__session = session
        self.__environ = environ or PyEnviron()
        self.__unit_of_work = unit_of_work or AlchemyUnitOfWork(session=self.__session)
        self.__customer_repository = customer_repository or PostgresCustomerRepository(session=self.__session)
        self.__user_repository = user_repository or PostgresUserRepository(session=self.__session)

    async def delete(self, customer_id: UUID):
        try:
            customer_deleter = CustomerDeleter(
                unit_of_work=self.__unit_of_work,
                customer_repository=self.__customer_repository,
                user_repository=self.__user_repository,
            )
            await customer_deleter.delete(customer_id=customer_id)
            response = {
                "success": True,
                "message": messages.SUCCESS_MESSAGE,
                "data": {}
            }, status.HTTP_200_OK

        except CustomerDoesNotExist as ex:
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
