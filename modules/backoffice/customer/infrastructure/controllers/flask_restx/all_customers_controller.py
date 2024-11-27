from modules.backoffice.customer.domain import CustomerRepository
from modules.backoffice.customer.application.all import AllCustomers
from modules.backoffice.customer.infrastructure.repositories.postgres import PostgresCustomerRepository
from modules.backoffice.customer.infrastructure.schemas.marshmallow import CustomerSchema
from modules.shared.serializer.domain import EntitySerializer
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.environ.domain import Environ
from modules.shared.environ.infraestructure import PyEnviron
from modules.shared.serializer.infraestructure.marshmallow import MarshmallowEntitySerializer


class AllCustomersController:
    """
    Class controller to get all Customers
    """

    def __init__(
        self,
        customer_repository: CustomerRepository = None,
        entity_serializer: EntitySerializer = None,
        environ: Environ = None
    ):
        """
        Args:
            customer_repository: repository for customer database table operations
            entity_serializer: serializer class
            environ: environ variable reader
        """

        self.__environ = environ or PyEnviron()
        self.__customer_repository = customer_repository or PostgresCustomerRepository(environ=self.__environ)
        self.__entity_serializer = entity_serializer or MarshmallowEntitySerializer(schema=CustomerSchema())

    def __call__(self):
        try:
            all_customers = AllCustomers(customer_repository=self.__customer_repository)
            all_customers = all_customers()
            customers = self.__entity_serializer(all_customers, many=True)
            response = {"success": True, "message": "OK", "data": customers}, status.HTTP_200_OK

        except Exception as ex:
            response = {
                "success": False,
                "message": messages.INTERNAL_SERVER_ERROR,
                "data": {}
            }, status.HTTP_500_INTERNAL_SERVER_ERROR
            return response

        else:
            return response
