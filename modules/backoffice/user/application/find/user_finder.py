from uuid import UUID
from modules.backoffice.user.domain import UserRepository
from modules.backoffice.user.domain import UserFinder as DomainUserFinder


class UserFinder:
    """
    Class to get User
    """

    def __init__(self, user_repository: UserRepository):
        """
        Args:
            user_repository: repository for user database table operations
        """

        self.__user_repository = user_repository

    async def find(self, user_id: UUID):
        user_finder = DomainUserFinder(user_repository=self.__user_repository)
        user = await user_finder.find(user_id=user_id)
        return user
