class UserDoesNotExist(Exception):
    ...


class WrongCredentials(Exception):
    ...


class ExpiredTokenError(Exception):
    ...


class InvalidTokenError(Exception):
    ...
