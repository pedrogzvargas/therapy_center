from uuid import UUID
from .user_repository import UserRepository
from .user_does_not_exist import UserDoesNotExist


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

    def __call__(self, user_id: UUID):
        user = self.__user_repository.get(id=user_id)

        if not user:
            raise UserDoesNotExist(f"User with id: {user_id} does not exist")

        return user
