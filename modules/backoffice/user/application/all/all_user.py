from modules.backoffice.user.domain import UserRepository


class AllUsers:
    """
    Class to get all Users
    """

    def __init__(self, user_repository: UserRepository):
        """
        Args:
            user_repository: repository for user database table operations
        """
        self.__user_repository= user_repository

    def __call__(self):
        return self.__user_repository.all()
