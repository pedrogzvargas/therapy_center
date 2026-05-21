from sqlalchemy.ext.asyncio import AsyncSession
from modules.shared.auth.domain import UserRepository
from modules.shared.password_hasher.domain import PasswordHasher
from modules.shared.auth.domain import TokenHandler
from modules.shared.auth.domain import UserDoesNotExist
from modules.shared.auth.domain import WrongCredentials
from modules.shared.persistence.domain import UnitOfWork
from modules.shared.auth.domain import RefreshTokenRepository
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.environ.domain import Environ
from modules.shared.serializer.domain import EntitySerializer
from modules.shared.auth.application import Login
from modules.shared.auth.infrastructure import PostgresRefreshTokenRepository
from modules.shared.auth.infrastructure import PostgresUserRepository
from modules.shared.auth.infrastructure import LoginSchema
from modules.shared.environ.infrastructure import PyEnviron
from modules.shared.serializer.infrastructure.marshmallow import MarshmallowEntitySerializer
from modules.shared.password_hasher.infrastructure import Argon2PasswordHasher
from modules.shared.persistence.infrastructure import AlchemyUnitOfWork
from modules.shared.auth.infrastructure import JwtTokenHandler


class LoginController:
    """
    Class controller to login
    """

    def __init__(
        self,
        session: AsyncSession,
        unit_of_work: UnitOfWork | None = None,
        user_repository: UserRepository | None = None,
        refresh_token_repository: RefreshTokenRepository | None = None,
        password_hasher: PasswordHasher | None = None,
        token_handler: TokenHandler | None = None,
        entity_serializer: EntitySerializer | None = None,
        environ: Environ | None = None
    ):
        """
        Args:
            user_repository: repository for user database table operations
            password_hasher: class to hash and verify password
            token_handler: class to create token
            entity_serializer: entity serializer
            environ: environ variable reader
        """

        self.__session = session
        self.__unit_of_work = unit_of_work or AlchemyUnitOfWork(session=self.__session)
        self.__environ = environ or PyEnviron()
        self.__user_repository = user_repository or PostgresUserRepository(session=self.__session)
        self.__refresh_token_repository = refresh_token_repository or PostgresRefreshTokenRepository(session=self.__session)
        self.__password_hasher = password_hasher or Argon2PasswordHasher()
        self.__token_handler = token_handler or JwtTokenHandler(self.__environ.get_str("SECRET_KEY"))
        self.__entity_serializer = entity_serializer or MarshmallowEntitySerializer(schema=LoginSchema())

    async def login(self, body: dict):
        try:
            login = Login(
                unit_of_work=self.__unit_of_work,
                user_repository=self.__user_repository,
                refresh_token_repository=self.__refresh_token_repository,
                password_hasher=self.__password_hasher,
                token_handler=self.__token_handler,
            )
            access_token, refresh_token = await login.login(username=body.get("username"), password=body.get("password"))
            login_response = self.__entity_serializer(dict(access_token=access_token, refresh_token=refresh_token))
            response = {
                "success": True,
                "message": messages.SUCCESS_MESSAGE,
                "data": login_response
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
