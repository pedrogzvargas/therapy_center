from uuid import UUID
from modules.backoffice.user.domain import UserRepository
from modules.backoffice.user.domain import UserDoesNotExist
from modules.backoffice.user.application.find import UserFinder
from modules.backoffice.user.infrastructure.repositories.postgres import PostgresUserRepository
from modules.backoffice.user.infrastructure.schemas.marshmallow import UserSchema
from modules.shared.serializer.domain import EntitySerializer
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.environ.domain import Environ
from modules.shared.environ.infraestructure import PyEnviron
from modules.shared.serializer.infraestructure.marshmallow import MarshmallowEntitySerializer


class UserFinderController:
    """
    Class controller to get User
    """

    def __init__(
        self,
        user_repository: UserRepository = None,
        entity_serializer: EntitySerializer = None,
        environ: Environ = None
    ):
        """
        Args:
            user_repository: repository for user database table operations
            entity_serializer: serializer class
            environ: environ variable reader
        """

        self.__environ = environ or PyEnviron()
        self.__user_repository = user_repository or PostgresUserRepository(environ=self.__environ)
        self.__entity_serializer = entity_serializer or MarshmallowEntitySerializer(schema=UserSchema())

    def __call__(self, user_id: UUID):
        try:
            user_finder = UserFinder(user_repository=self.__user_repository)
            user = user_finder(user_id=user_id)
            user = self.__entity_serializer(user)
            response = {
                "success": True,
                "message": messages.SUCCESS_MESSAGE,
                "data": user
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
