from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from modules.backoffice.customer.domain import CustomerRepository
from modules.backoffice.customer.domain import CustomerDoesNotExist
from modules.backoffice.customer.application import CustomerFinder
from modules.backoffice.customer.infrastructure.repositories import PostgresCustomerRepository
from modules.backoffice.customer.infrastructure.schemas.marshmallow import CustomerSchema
from modules.shared.serializer.domain import EntitySerializer
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.environ.domain import Environ
from modules.shared.environ.infrastructure import PyEnviron
from modules.shared.serializer.infrastructure.marshmallow import MarshmallowEntitySerializer


class CustomerFinderController:
    """
    Class controller to get Customer
    """

    def __init__(
        self,
        session: AsyncSession,
        customer_repository: CustomerRepository | None = None,
        entity_serializer: EntitySerializer | None = None,
        environ: Environ | None = None
    ):
        """
        Args:
            customer_repository: repository for customer database table operations
            entity_serializer: serializer class
            environ: environ variable reader
        """

        self.__environ = environ or PyEnviron()
        self.__session = session
        self.__customer_repository = customer_repository or PostgresCustomerRepository(session=self.__session)
        self.__entity_serializer = entity_serializer or MarshmallowEntitySerializer(schema=CustomerSchema())

    def __call__(self, customer_id: UUID):
        return self.find(customer_id)

    async def find(self, customer_id: UUID):
        try:
            customer_finder = CustomerFinder(customer_repository=self.__customer_repository)
            customer = await customer_finder.find(customer_id=customer_id)
            customer = self.__entity_serializer(customer)
            response = {
                "success": True,
                "message": messages.SUCCESS_MESSAGE,
                "data": customer
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
