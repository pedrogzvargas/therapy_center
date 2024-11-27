from modules.app.user.domain import UserRepository
from modules.shared.password_hasher.domain import PasswordHasher
from modules.shared.auth.domain import TokenHandler
from modules.app.user.domain import UserDoesNotExist
from modules.app.auth.domain import WrongCredentials
from modules.app.auth.application import Login
from modules.app.user.infrastructure.repositories.postgres import PostgresUserRepository
from modules.app.auth.infrastructure.schemas.marshmallow import TokenSchema
from modules.shared.serializer.domain import EntitySerializer
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.environ.domain import Environ
from modules.shared.environ.infraestructure import PyEnviron
from modules.shared.serializer.infraestructure.marshmallow import MarshmallowEntitySerializer
from modules.shared.password_hasher.infraestructure import Argon2PasswordHasher
from modules.shared.auth.infraestructure import JwtTokenHandler


class LoginController:
    """
    Class controller to login
    """

    def __init__(
        self,
        user_repository: UserRepository = None,
        password_hasher: PasswordHasher = None,
        token_handler: TokenHandler = None,
        entity_serializer: EntitySerializer = None,
        environ: Environ = None
    ):
        """
        Args:
            user_repository: repository for user database table operations
            password_hasher: class to hash and verify password
            token_handler: class to create token
            entity_serializer: entity serializer
            environ: environ variable reader
        """

        self.__environ = environ or PyEnviron()
        self.__user_repository = user_repository or PostgresUserRepository(environ=self.__environ)
        self.__password_hasher = password_hasher or Argon2PasswordHasher()
        self.__token_handler = token_handler or JwtTokenHandler(self.__environ.get_str("SECRET_KEY"))
        self.__entity_serializer = entity_serializer or MarshmallowEntitySerializer(schema=TokenSchema())

    def __call__(self, body: dict):
        try:
            login = Login(
                user_repository=self.__user_repository,
                password_hasher=self.__password_hasher,
                token_handler=self.__token_handler,
            )
            token = login(username=body.get("username"), password=body.get("password"))
            token_response = self.__entity_serializer(dict(token=token))
            response = {
                "success": True,
                "message": messages.SUCCESS_MESSAGE,
                "data": token_response
            }, status.HTTP_200_OK

        except (UserDoesNotExist, WrongCredentials) as ex:
            response = {
                "success": False,
                "message": f"{messages.WRONG_CREDENTIALS}",
                "data": {}
            }, status.HTTP_400_BAD_REQUEST
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
