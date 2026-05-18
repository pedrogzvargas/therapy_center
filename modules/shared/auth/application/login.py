from datetime import datetime
from datetime import timezone
from datetime import timedelta
from modules.shared.password_hasher.domain import PasswordHasher
from modules.shared.auth.domain import TokenHandler
from modules.shared.auth.domain import UserRepository
from modules.shared.auth.domain import UserDoesNotExist
from modules.shared.auth.domain import WrongCredentials


class Login:

    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        token_handler: TokenHandler,
    ):

        self.__user_repository = user_repository
        self.__password_hasher = password_hasher
        self.__token_handler = token_handler

    async def login(self, username, password):
        user = await self.__user_repository.get_by_username(username=username)

        if not user:
            raise UserDoesNotExist(f"User with username: {username} does not exist")

        if not self.__password_hasher.verify(hashed_password=user.password, password=password):
            raise WrongCredentials(f"Wrong credentials")

        access_token_payload = dict(
            sub=str(user.id),
            type="access",
            iat=datetime.now(timezone.utc),
            exp=datetime.now(timezone.utc) + timedelta(minutes=15),
        )

        refresh_token_payload = dict(
            sub=str(user.id),
            type="refresh",
            iat=datetime.now(timezone.utc),
            exp=datetime.now(timezone.utc) + timedelta(hours=24),
        )

        access_token = self.__token_handler.encode(payload=access_token_payload)
        refresh_token = self.__token_handler.encode(payload=refresh_token_payload)

        return access_token, refresh_token
