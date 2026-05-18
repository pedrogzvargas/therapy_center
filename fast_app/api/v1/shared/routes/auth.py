from fastapi import APIRouter
from fastapi import Response
from fastapi import Depends
from modules.shared.auth.infrastructure import LoginController
from modules.shared.auth.infrastructure import LogoutController
from modules.shared.auth.infrastructure import RefreshTokenController
from fast_app.api.v1.shared.scehmas.auth import Login
from fast_app.api.v1.shared.scehmas.auth import Logout
from fast_app.api.v1.shared.scehmas.auth import RefreshToken
from fast_app.core.db_session import get_session

router = APIRouter()

@router.post("/login")
async def login(response: Response, payload: Login, db_session = Depends(get_session)):
    login_controller = LoginController(session=db_session)
    controller_response, code = await login_controller.login(body=payload.model_dump())
    response.status_code = code
    return controller_response

@router.post("/logout")
def login(response: Response, payload: Logout, db_session = Depends(get_session)):
    logout_controller = LogoutController()
    controller_response, code = logout_controller.logout(body=payload.model_dump())
    response.status_code = code
    return controller_response

@router.post("/refresh-token")
def refresh_token(response: Response, payload: RefreshToken):
    refresh_token_controller = RefreshTokenController()
    controller_response, code = refresh_token_controller.refresh(body=payload.model_dump())
    response.status_code = code
    return controller_response
