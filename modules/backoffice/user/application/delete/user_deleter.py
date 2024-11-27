from uuid import UUID
from modules.backoffice.user.domain import UserRepository
from modules.backoffice.user.domain import UserFinder as DomainUserFinder


class UserDeleter:
    """
    Class to delete User
    """

    def __init__(self, user_repository: UserRepository):
        """
        Args:
            user_repository: repository for user database table operations
        """
        self.__user_repository = user_repository

    def __call__(self, user_id: UUID):
        user_finder = DomainUserFinder(user_repository=self.__user_repository)
        user = user_finder(user_id=user_id)
        self.__user_repository.delete(user)
