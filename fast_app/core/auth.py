from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials
from modules.shared.auth.infrastructure import JwtTokenHandler
from modules.shared.environ.infrastructure import PyEnviron
from modules.shared.auth.domain.exceptions import ExpiredTokenError

security = HTTPBearer()
environ = PyEnviron()
token_handler = JwtTokenHandler(environ.get_str("SECRET_KEY"))

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        payload = token_handler.decode(token)
        return payload

    except ExpiredTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expired token",
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

def require_permission(permission: str):
    async def dependency(current_user = Depends(get_current_user), ):
        permissions = current_user.get("permissions", [])

        if permission not in permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied",
            )

        return current_user

    return dependency
