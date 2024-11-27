from modules.shared.password_hasher.domain import PasswordHasher
from modules.shared.auth.domain import TokenHandler
from modules.app.user.domain import UserRepository
from modules.app.user.domain import UserDoesNotExist
from modules.app.auth.domain import WrongCredentials


class Login:

    def __init__(
        self,
        user_repository: UserRepository = None,
        password_hasher: PasswordHasher = None,
        token_handler: TokenHandler = None,
    ):

        self.__user_repository = user_repository
        self.__password_hasher = password_hasher
        self.__token_handler = token_handler

    def __call__(self, username, password):
        user = self.__user_repository.get_by_username(username=username)

        if not user:
            raise UserDoesNotExist(f"User with username: {username} does not exist")

        if not self.__password_hasher.verify(hashed_password=user.password, password=password):
            raise WrongCredentials(f"Wrong credentials")

        token_payload = dict(user_id=str(user.id),)
        token = self.__token_handler.encode(payload=token_payload)

        return token
