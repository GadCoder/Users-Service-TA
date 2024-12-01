import json
import uuid

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


@router.get("/get-by-code/")
@inject
def get_by_admin_code(
        admin_code: uuid.UUID,
        admin_service: AdminServiceInterface = Depends(Provide[Container.admin_service]),
):
    response = admin_service.get_by_code(admin_code=admin_code)
    data = jsonable_encoder(response.value)
    return Response(
        content=json.dumps(data),
        media_type="application/json",
        status_code=STATUS_CODES[response.type],
    )


@router.get("/get-by-email/")
@inject
def get_by_admin_code(
        email: str,
        admin_service: AdminServiceInterface = Depends(Provide[Container.admin_service]),
):
    response = admin_service.get_by_email(email=email)
    data = jsonable_encoder(response.value)
    return Response(
        content=json.dumps(data),
        media_type="application/json",
        status_code=STATUS_CODES[response.type],
    )
