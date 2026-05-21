from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials
from modules.shared.auth.infrastructure import JwtTokenHandler
from modules.shared.environ.infrastructure import PyEnviron
from modules.shared.auth.domain import ExpiredTokenError

security = HTTPBearer()
environ = PyEnviron()
token_handler = JwtTokenHandler(environ.get_str("SECRET_KEY"))

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        payload = token_handler.decode(token)
        return {
            "user_id": payload.get("sub"),
            "jti": payload.get("jti"),
        }

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
