import json

from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, Response
from dependency_injector.wiring import Provide, inject

from src.app.domain.schemas.admin import AdminCreate
from src.app.configurator.containers import Container
from src.app.domain.ports.use_cases.admin import AdminServiceInterface
from src.app.adapters.entrypoints.response_status_codes import STATUS_CODES

router = APIRouter()


@router.post("/create/")
@inject
def create_admin(
        admin: AdminCreate,
        admin_service: AdminServiceInterface = Depends(Provide[Container.admin_service]),
):
    response = admin_service.create(admin=admin)
    data = jsonable_encoder(response.value)
    return Response(
        content=json.dumps(data),
        media_type="application/json",
        status_code=STATUS_CODES[response.type],
    )
