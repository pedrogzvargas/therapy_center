from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from modules.backoffice.user.domain import UserRepository
from modules.backoffice.user.domain import UserDoesNotExist
from modules.backoffice.user.application.find import UserFinder
from modules.backoffice.user.infrastructure.repositories import PostgresUserRepository
from modules.backoffice.user.infrastructure.schemas.marshmallow import UserSchema
from modules.shared.serializer.domain import EntitySerializer
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.environ.domain import Environ
from modules.shared.environ.infrastructure import PyEnviron
from modules.shared.serializer.infrastructure.marshmallow import MarshmallowEntitySerializer


class UserFinderController:
    """
    Class controller to get User
    """

    def __init__(
        self,
        session: AsyncSession,
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
        self.__session = session
        self.__user_repository = user_repository or PostgresUserRepository(session=self.__session)
        self.__entity_serializer = entity_serializer or MarshmallowEntitySerializer(schema=UserSchema())

    async def find(self, user_id: UUID):
        try:
            user_finder = UserFinder(user_repository=self.__user_repository)
            user = await user_finder.find(user_id=user_id)
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
