from uuid import UUID
from fastapi import APIRouter
from fastapi import Response
from fastapi import Depends
from typing import Annotated
from modules.backoffice.payment_method.infrastructure.controllers import PaymentMethodSearcherController
from modules.backoffice.payment_method.infrastructure.controllers import PaymentMethodCreatorController
from modules.backoffice.payment_method.infrastructure.controllers import PaymentMethodFinderController
from modules.backoffice.payment_method.infrastructure.controllers import PaymentMethodPatcherController
from modules.backoffice.payment_method.infrastructure.controllers import PaymentMethodDeleterController
from fast_app.api.v1.backoffice.schemas import PaymentMethodQueryParams
from fast_app.api.v1.backoffice.schemas import PaymentMethod
from fast_app.api.v1.backoffice.schemas import PatchPaymentMethod
from fast_app.core.db_session import get_session

router = APIRouter()

@router.post("/payment-method")
async def create_payment_method(response: Response, payment_method: PaymentMethod, db_session = Depends(get_session),):
    payment_method_creator_controller = PaymentMethodCreatorController(session=db_session)
    controller_response, code = await payment_method_creator_controller.create(body=payment_method.model_dump())
    response.status_code = code
    return controller_response

@router.get("/payment-method")
async def list_payment_method(
    response: Response,
    query_params: Annotated[PaymentMethodQueryParams, Depends()],
    db_session = Depends(get_session),
):
    query_params = query_params.model_dump(exclude_none=True)
    payment_method_searcher_controller = PaymentMethodSearcherController(session=db_session)
    controller_response, code = await payment_method_searcher_controller.search(query_params=query_params)
    response.status_code = code
    return controller_response

@router.get("/payment-method/{payment_method_id}")
async def get_payment_method(response: Response, payment_method_id: UUID, db_session = Depends(get_session),):
    payment_method_finder_controller = PaymentMethodFinderController(session=db_session)
    controller_response, code = await payment_method_finder_controller.find(payment_method_id=payment_method_id)
    response.status_code = code
    return controller_response

@router.patch("/payment-method/{payment_method_id}")
async def patch_payment_method(
    response: Response,
    payment_method_id: UUID,
    payment_method: PatchPaymentMethod,
    db_session = Depends(get_session),
):
    payment_method_patcher_controller = PaymentMethodPatcherController(session=db_session)
    controller_response, code = await payment_method_patcher_controller.patch(
        payment_method_id=payment_method_id,
        data=payment_method.model_dump(exclude_none=True),
    )
    response.status_code = code
    return controller_response

@router.delete("/payment-method/{payment_method_id}")
async def delete_payment_method(response: Response, payment_method_id: UUID, db_session = Depends(get_session),):
    payment_method_deleter_controller = PaymentMethodDeleterController(session=db_session)
    controller_response, code = await payment_method_deleter_controller.delete(payment_method_id=payment_method_id)
    response.status_code = code
    return controller_response
