from uuid import UUID
from modules.backoffice.user.domain import UserRepository
from modules.backoffice.user.domain import UserDoesNotExist
from modules.backoffice.user.application.delete import UserDeleter
from modules.backoffice.user.infrastructure.repositories.postgres import PostgresUserRepository
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.environ.domain import Environ
from modules.shared.environ.infraestructure import PyEnviron


class UserDeleterController:
    """
    Class controller to delete User
    """

    def __init__(
        self,
        user_repository: UserRepository = None,
        environ: Environ = None
    ):
        """
        Args:
            user_repository: repository for user database table operations
            environ: environ variable reader
        """

        self.__environ = environ or PyEnviron()
        self.__user_repository = user_repository or PostgresUserRepository(environ=self.__environ)

    def __call__(self, user_id: UUID):
        try:
            user_deleter = UserDeleter(user_repository=self.__user_repository)
            user_deleter(user_id=user_id)
            response = {
                "success": True,
                "message": messages.SUCCESS_MESSAGE,
                "data": {}
            }, status.HTTP_200_OK

        except UserDoesNotExist as ex:
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
