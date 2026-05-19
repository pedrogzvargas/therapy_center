from uuid import UUID
from fastapi import APIRouter
from fastapi import Response
from fastapi import Depends
from modules.backoffice.user.infrastructure.controllers import UserFinderController
from fast_app.core.db_session import get_session

router = APIRouter()

@router.get("/user/{user_id}")
async def get_user(response: Response, user_id: UUID, db_session = Depends(get_session),):
    user_finder_controller = UserFinderController(session=db_session)
    controller_response, code = await user_finder_controller.find(user_id=user_id)
    response.status_code = code
    return controller_response
