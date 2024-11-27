from jwt import encode
from jwt import decode
from modules.shared.auth.domain import TokenHandler


class JwtTokenHandler(TokenHandler):

    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.__secret_key = secret_key
        self.__algorithm = algorithm

    def encode(self, payload):
        return encode(key=self.__secret_key, payload=payload, algorithm=self.__algorithm)

    def decode(self, token):
        return decode(jwt=token, key=self.__secret_key, algorithms=self.__algorithm)
