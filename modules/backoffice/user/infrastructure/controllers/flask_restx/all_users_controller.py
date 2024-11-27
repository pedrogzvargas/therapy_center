from modules.backoffice.user.domain import UserRepository
from modules.backoffice.user.application.all import AllUsers
from modules.backoffice.user.infrastructure.repositories.postgres import PostgresUserRepository
from modules.backoffice.user.infrastructure.schemas.marshmallow import UserSchema
from modules.shared.serializer.domain import EntitySerializer
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.environ.domain import Environ
from modules.shared.environ.infraestructure import PyEnviron
from modules.shared.serializer.infraestructure.marshmallow import MarshmallowEntitySerializer


class AllUsersController:
    """
    Class controller to get all Users
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

    def __call__(self):
        try:
            all_users = AllUsers(user_repository=self.__user_repository)
            all_users = all_users()
            users = self.__entity_serializer(all_users, many=True)
            response = {"success": True, "message": "OK", "data": users}, status.HTTP_200_OK

        except Exception as ex:
            response = {
                "success": False,
                "message": messages.INTERNAL_SERVER_ERROR,
                "data": {}
            }, status.HTTP_500_INTERNAL_SERVER_ERROR
            return response

        else:
            return response
