from uuid import UUID
from fastapi import APIRouter
from fastapi import Response
from fastapi import Depends
from typing import Annotated
from modules.backoffice.customer.infrastructure.controllers import CustomerSearcherController
from modules.backoffice.customer.infrastructure.controllers import CustomerFinderController
from modules.backoffice.customer.infrastructure.controllers import CustomerCreatorController
from modules.backoffice.customer.infrastructure.controllers import CustomerDeleterController
from fast_app.api.v1.backoffice.schemas import Customer
from fast_app.api.v1.backoffice.schemas import CustomerQueryParams
from fast_app.core.db_session import get_session
from fast_app.core.auth import require_permission

router = APIRouter()

@router.post("/customer")
async def create_customer(
    response: Response,
    customer: Customer,
    db_session = Depends(get_session),
    dependencies = (Depends(require_permission("customer:create"))),
):
    customer_creator_controller = CustomerCreatorController(session=db_session)
    controller_response, code = await customer_creator_controller.create(body=customer.model_dump())
    response.status_code = code
    return controller_response

@router.get("/customer")
async def list_customers(
    response: Response,
    query_params: Annotated[CustomerQueryParams, Depends()],
    db_session = Depends(get_session),
    dependencies = (Depends(require_permission("customer:list"))),
):
    query_params = query_params.model_dump(exclude_none=True)
    customer_searcher_controller = CustomerSearcherController(session=db_session)
    controller_response, code = await customer_searcher_controller.search(query_params=query_params)
    response.status_code = code
    return controller_response

@router.get("/customer/{customer_id}")
async def get_customer(response: Response, customer_id: UUID, db_session = Depends(get_session),):
    customer_finder_controller = CustomerFinderController(session=db_session)
    controller_response, code = await customer_finder_controller.find(customer_id=customer_id)
    response.status_code = code
    return controller_response

@router.delete("/customer/{customer_id}")
async def delete_customer(response: Response, customer_id: UUID, db_session = Depends(get_session),):
    customer_deleter_controller = CustomerDeleterController(session=db_session)
    controller_response, code = await customer_deleter_controller.delete(customer_id=customer_id)
    response.status_code = code
    return controller_response
