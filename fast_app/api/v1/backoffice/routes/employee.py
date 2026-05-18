from uuid import UUID
from fastapi import APIRouter
from fastapi import Response
from fastapi import Depends
from typing import Annotated
from modules.backoffice.employee.infrastructure.controllers import EmployeeCreatorController
from modules.backoffice.employee.infrastructure.controllers import EmployeeSearcherController
from modules.backoffice.employee.infrastructure.controllers import EmployeeFinderController
from modules.backoffice.employee.infrastructure.controllers import EmployeeDeleterController
from fast_app.api.v1.backoffice.schemas import Employee
from fast_app.api.v1.backoffice.schemas import EmployeeQueryParams
from fast_app.core.db_session import get_session

router = APIRouter()

@router.post("/employee")
async def create_employee(response: Response, employee: Employee, db_session = Depends(get_session),):
    employee_creator_controller = EmployeeCreatorController(session=db_session)
    controller_response, code = await employee_creator_controller.create(body=employee.model_dump())
    response.status_code = code
    return controller_response

@router.get("/employee")
async def list_employees(
    response: Response,
    query_params: Annotated[EmployeeQueryParams, Depends()],
    db_session = Depends(get_session),
):
    query_params = query_params.model_dump(exclude_none=True)
    employee_searcher_controller = EmployeeSearcherController(session=db_session)
    controller_response, code = await employee_searcher_controller.search(query_params=query_params)
    response.status_code = code
    return controller_response

@router.get("/employee/{employee_id}")
async def get_employee(response: Response, employee_id: UUID, db_session = Depends(get_session),):
    employee_finder_controller = EmployeeFinderController(session=db_session)
    controller_response, code = await employee_finder_controller.find(employee_id=employee_id)
    response.status_code = code
    return controller_response

@router.delete("/employee/{employee_id}")
async def delete_employee(response: Response, employee_id: UUID, db_session = Depends(get_session),):
    employee_deleter_controller = EmployeeDeleterController(session=db_session)
    controller_response, code = await employee_deleter_controller.delete(employee_id=employee_id)
    response.status_code = code
    return controller_response
