from flask import request
from flask import g
import jwt

from modules.shared.environ.infraestructure import PyEnviron
from modules.shared.http.domain import messages
from modules.shared.http.domain import status

from functools import wraps


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        environ = PyEnviron()
        token = request.headers.get("Authorization")
        if not token:
            return {"success": False, "message": messages.MISSING_TOKEN, "data": {}}, status.HTTP_403_FORBIDDEN
        try:
            token = token.split(" ")[1]
            decoded_token = jwt.decode(token, environ.get_str("SECRET_KEY"), algorithms=["HS256"])
            g.user = decoded_token
        except jwt.ExpiredSignatureError:
            return {"success": False, "message": messages.EXPIRED_TOKEN, "data": {}}, status.HTTP_403_FORBIDDEN
        except jwt.InvalidTokenError:
            return {"success": False, "message": messages.INVALID_TOKEN, "data": {}}, status.HTTP_403_FORBIDDEN
        return f(*args, **kwargs)
    return decorated_function
