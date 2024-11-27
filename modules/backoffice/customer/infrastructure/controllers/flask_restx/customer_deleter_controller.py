from uuid import UUID
from modules.backoffice.customer.domain import CustomerRepository
from modules.backoffice.customer.domain import CustomerDoesNotExist
from modules.backoffice.customer.application.delete import CustomerDeleter
from modules.backoffice.customer.infrastructure.repositories.postgres import PostgresCustomerRepository
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.environ.domain import Environ
from modules.shared.environ.infraestructure import PyEnviron


class CustomerDeleterController:
    """
    Class controller to delete Customer
    """

    def __init__(
        self,
        customer_repository: CustomerRepository = None,
        environ: Environ = None
    ):
        """
        Args:
            customer_repository: repository for customer database table operations
            environ: environ variable reader
        """

        self.__environ = environ or PyEnviron()
        self.__customer_repository = customer_repository or PostgresCustomerRepository(environ=self.__environ)

    def __call__(self, customer_id: UUID):
        try:
            customer_deleter = CustomerDeleter(customer_repository=self.__customer_repository)
            customer_deleter(customer_id=customer_id)
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
