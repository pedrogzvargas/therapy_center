from modules.shared.auth.domain import TokenHandler
from modules.shared.auth.domain import InvalidTokenError


class Logout:

    def __init__(self, token_handler: TokenHandler):
        self.__token_handler = token_handler

    def logout(self, token):
        refresh_token_payload = self.__token_handler.decode(token)
        jti = refresh_token_payload.get("jti")
        token_type = refresh_token_payload.get("type")

        if token_type != "access":
            raise InvalidTokenError("Invalid token")
