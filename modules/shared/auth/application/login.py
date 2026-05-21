import uuid
from datetime import datetime
from datetime import timezone
from datetime import timedelta
from modules.shared.persistence.domain import UnitOfWork
from modules.shared.password_hasher.domain import PasswordHasher
from modules.shared.auth.domain import RefreshToken
from modules.shared.auth.domain import TokenHandler
from modules.shared.auth.domain import UserRepository
from modules.shared.auth.domain import RefreshTokenRepository
from modules.shared.auth.domain import UserDoesNotExist
from modules.shared.auth.domain import WrongCredentials


class Login:

    def __init__(
        self,
        unit_of_work: UnitOfWork,
        user_repository: UserRepository,
        refresh_token_repository: RefreshTokenRepository,
        password_hasher: PasswordHasher,
        token_handler: TokenHandler,
    ):

        self.__user_repository = user_repository
        self.__refresh_token_repository = refresh_token_repository
        self.__unit_of_work = unit_of_work
        self.__password_hasher = password_hasher
        self.__token_handler = token_handler

    async def login(self, username, password):
        user = await self.__user_repository.get_by_username(username=username)

        if not user:
            raise UserDoesNotExist(f"User with username: {username} does not exist")

        if not self.__password_hasher.verify(hashed_password=user.password, password=password):
            raise WrongCredentials(f"Wrong credentials")

        jti = uuid.uuid4()

        access_token_payload = dict(
            sub=str(user.id),
            type="access",
            jti=str(jti),
            iat=datetime.now(timezone.utc),
            exp=datetime.now(timezone.utc) + timedelta(minutes=15),
        )

        refresh_token_payload = dict(
            sub=str(user.id),
            type="refresh",
            jti=str(jti),
            iat=datetime.now(timezone.utc),
            exp=datetime.now(timezone.utc) + timedelta(hours=24),
        )

        access_token = self.__token_handler.encode(payload=access_token_payload)
        refresh_token = self.__token_handler.encode(payload=refresh_token_payload)
        refresh_token_entity = RefreshToken.create(id=jti, user_id=user.id, jti=jti)

        async with self.__unit_of_work:
            await self.__refresh_token_repository.add(refresh_token=refresh_token_entity)

        return access_token, refresh_token
