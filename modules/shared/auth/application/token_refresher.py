from uuid import uuid4
from datetime import datetime
from datetime import timezone
from datetime import timedelta
from modules.shared.auth.domain import TokenHandler
from modules.shared.auth.domain import InvalidTokenError


class TokenRefresher:

    def __init__(self, token_handler: TokenHandler):
        self.__token_handler = token_handler

    def refresh(self, token):
        refresh_token_payload = self.__token_handler.decode(token)
        user_id = refresh_token_payload.get("sub")
        token_type = refresh_token_payload.get("type")

        if token_type != "refresh":
            raise InvalidTokenError("Invalid token")

        access_token_payload = dict(
            sub=str(user_id),
            jti=str(uuid4()),
            type="access",
            iat=datetime.now(timezone.utc),
            exp=datetime.now(timezone.utc) + timedelta(minutes=15),
        )

        refresh_token_payload = dict(
            sub=str(user_id),
            jti=str(uuid4()),
            type="refresh",
            iat=datetime.now(timezone.utc),
            exp=datetime.now(timezone.utc) + timedelta(hours=24),
        )

        access_token = self.__token_handler.encode(payload=access_token_payload)
        refresh_token = self.__token_handler.encode(payload=refresh_token_payload)

        return access_token, refresh_token
