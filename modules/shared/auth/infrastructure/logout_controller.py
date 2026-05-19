from modules.shared.auth.domain import TokenHandler
from modules.shared.auth.application import Logout
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.auth.domain import ExpiredTokenError
from modules.shared.auth.domain import InvalidTokenError
from modules.shared.environ.domain import Environ
from modules.shared.environ.infrastructure import PyEnviron
from modules.shared.auth.infrastructure import JwtTokenHandler


class LogoutController:
    """
    Class controller to logout
    """

    def __init__(
        self,
        token_handler: TokenHandler | None = None,
        environ: Environ | None = None
    ):
        """
        Args:
            token_handler: class to create token
            environ: environ variable reader
        """

        self.__environ = environ or PyEnviron()
        self.__token_handler = token_handler or JwtTokenHandler(self.__environ.get_str("SECRET_KEY"))

    def logout(self, body: dict):
        try:
            logout = Logout(token_handler=self.__token_handler)
            logout.logout(token=body.get("access_token"))
            response = {
                "success": True,
                "message": messages.SUCCESS_MESSAGE,
                "data": {}
            }, status.HTTP_200_OK

        except ExpiredTokenError as ex:
            response = {
                "success": False,
                "message": f"{messages.EXPIRED_TOKEN}",
                "data": {}
            }, status.HTTP_401_UNAUTHORIZED
            return response

        except InvalidTokenError as ex:
            response = {
                "success": False,
                "message": f"{messages.INVALID_TOKEN}",
                "data": {}
            }, status.HTTP_400_BAD_REQUEST
            return response

        except Exception as ex:
            response = {
                "success": False,
                "message": messages.INTERNAL_SERVER_ERROR,
                "data": {}
            }, status.HTTP_500_INTERNAL_SERVER_ERROR
            return response

        else:
            return response
