from modules.backoffice.customer.domain import CustomerRepository
from modules.backoffice.customer.application.search import SearchCustomers
from modules.backoffice.customer.infrastructure.repositories.postgres import PostgresCustomerRepository
from modules.backoffice.customer.infrastructure.schemas.marshmallow import SearchCustomerSchema
from modules.shared.serializer.domain import EntitySerializer
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.environ.domain import Environ
from modules.shared.logger.domain import Logger
from modules.shared.environ.infraestructure import PyEnviron
from modules.shared.serializer.infraestructure.marshmallow import MarshmallowEntitySerializer
from modules.shared.logger.infraestructure import PyLogger


class SearchCustomersController:
    """
    Class controller to search Customers
    """

    def __init__(
        self,
        customer_repository: CustomerRepository = None,
        entity_serializer: EntitySerializer = None,
        environ: Environ = None,
        logger: Logger = None,
    ):
        """
        Args:
            customer_repository: repository for customer database table operations
            entity_serializer: serializer class
            environ: environ variable reader
            logger: logger
        """

        self.__environ = environ or PyEnviron()
        self.__customer_repository = customer_repository or PostgresCustomerRepository(environ=self.__environ)
        self.__entity_serializer = entity_serializer or MarshmallowEntitySerializer(schema=SearchCustomerSchema())
        self.__logger = logger or PyLogger(
            level=self.__environ.get_str("LOG_LEVEL"),
            format=self.__environ.get_str("LOG_FORMAT"),
        )

    def __call__(self, query_params: dict, page: int, page_size: int):
        try:
            search_customers = SearchCustomers(customer_repository=self.__customer_repository)
            customers = search_customers(query_params=query_params, page_size=page_size, page=page)
            customers = self.__entity_serializer(customers)
            response = customers, status.HTTP_200_OK

        except Exception as ex:
            self.__logger.error(f"UserCreatorController: {ex}")
            response = {
                "success": False,
                "message": messages.INTERNAL_SERVER_ERROR,
                "data": {}
            }, status.HTTP_500_INTERNAL_SERVER_ERROR
            return response

        else:
            return response
