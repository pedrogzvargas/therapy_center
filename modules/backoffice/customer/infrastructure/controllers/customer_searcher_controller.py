from sqlalchemy.ext.asyncio import AsyncSession
from modules.backoffice.customer.domain import CustomerRepository
from modules.backoffice.customer.application import CustomerSearcher
from modules.backoffice.customer.infrastructure.repositories import PostgresCustomerRepository
from modules.backoffice.customer.infrastructure.schemas.marshmallow import SearchCustomerSchema
from modules.shared.serializer.domain import EntitySerializer
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.environ.domain import Environ
from modules.shared.logger.domain import Logger
from modules.shared.environ.infrastructure import PyEnviron
from modules.shared.serializer.infrastructure.marshmallow import MarshmallowEntitySerializer
from modules.shared.logger.infrastructure import PyLogger


class CustomerSearcherController:
    """
    Class controller to search Customers
    """

    def __init__(
        self,
        session: AsyncSession,
        customer_repository: CustomerRepository | None = None,
        entity_serializer: EntitySerializer | None = None,
        environ: Environ | None = None,
        logger: Logger | None = None,
    ):
        """
        Args:
            customer_repository: repository for customer database table operations
            entity_serializer: serializer class
            environ: environ variable reader
            logger: logger
        """

        self.__session = session
        self.__environ = environ or PyEnviron()
        self.__customer_repository = customer_repository or PostgresCustomerRepository(session=self.__session)
        self.__entity_serializer = entity_serializer or MarshmallowEntitySerializer(schema=SearchCustomerSchema())
        self.__logger = logger or PyLogger(
            level=self.__environ.get_str("LOG_LEVEL"),
            format=self.__environ.get_str("LOG_FORMAT"),
        )

    async def search(self, query_params: dict):
        try:
            search_customers = CustomerSearcher(customer_repository=self.__customer_repository)
            customers = await search_customers.search(query_params=query_params)
            customers = self.__entity_serializer(customers)
            response = customers, status.HTTP_200_OK

        except Exception as ex:
            self.__logger.error(f"SearchCustomersController: {ex}")
            response = {
                "success": False,
                "message": messages.INTERNAL_SERVER_ERROR,
                "data": {}
            }, status.HTTP_500_INTERNAL_SERVER_ERROR
            return response

        else:
            return response
