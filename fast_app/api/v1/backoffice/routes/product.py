from uuid import UUID
from fastapi import APIRouter
from fastapi import Response
from fastapi import Depends
from typing import Annotated
from modules.backoffice.product.infrastructure.controllers import ProductCreatorController
from modules.backoffice.product.infrastructure.controllers import ProductFinderController
from modules.backoffice.product.infrastructure.controllers import ProductSearcherController
from modules.backoffice.product.infrastructure.controllers import ProductPatcherController
from modules.backoffice.product.infrastructure.controllers import ProductDeleterController
from fast_app.api.v1.backoffice.schemas import ProductQueryParams
from fast_app.api.v1.backoffice.schemas import Product
from fast_app.api.v1.backoffice.schemas import PatchProduct
from fast_app.core.db_session import get_session

router = APIRouter()

@router.post("/product")
async def create_product(response: Response, product: Product, db_session = Depends(get_session),):
    product_creator_controller = ProductCreatorController(session=db_session)
    controller_response, code = await product_creator_controller.create(body=product.model_dump())
    response.status_code = code
    return controller_response

@router.get("/product")
async def list_products(
    response: Response,
    query_params: Annotated[ProductQueryParams, Depends()],
    db_session = Depends(get_session),
):
    query_params = query_params.model_dump(exclude_none=True)
    product_searcher_controller = ProductSearcherController(session=db_session)
    controller_response, code = await product_searcher_controller.search(query_params=query_params)
    response.status_code = code
    return controller_response

@router.get("/product/{product_id}")
async def get_product(response: Response, product_id: UUID, db_session = Depends(get_session),):
    product_finder_controller = ProductFinderController(session=db_session)
    controller_response, code = await product_finder_controller.find(product_id=product_id)
    response.status_code = code
    return controller_response

@router.patch("/product/{product_id}")
async def patch_product(
    response: Response,
    product_id: UUID,
    product: PatchProduct,
    db_session = Depends(get_session),
):
    product_patcher_controller = ProductPatcherController(session=db_session)
    controller_response, code = await product_patcher_controller.patch(
        product_id=product_id,
        data=product.model_dump(exclude_none=True),
    )
    response.status_code = code
    return controller_response

@router.delete("/product/{product_id}")
async def delete_product(response: Response, product_id: UUID, db_session = Depends(get_session),):
    product_deleter_controller = ProductDeleterController(session=db_session)
    controller_response, code = await product_deleter_controller.delete(product_id=product_id)
    response.status_code = code
    return controller_response
