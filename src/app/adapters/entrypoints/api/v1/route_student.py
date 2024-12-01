import json

from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, Response, HTTPException, status
from dependency_injector.wiring import Provide, inject

from src.app.domain.models.user import User
from src.app.configurator.containers import Container
from src.app.domain.schemas.student import StudentCreate
from src.app.domain.ports.use_cases.student import StudentServiceInterface
from src.app.adapters.entrypoints.response_status_codes import STATUS_CODES
from src.app.adapters.entrypoints.api.v1.route_login import get_current_user_from_token

router = APIRouter()


@router.post("/create/")
@inject
async def create_user(
        student: StudentCreate,
        current_user: User = Depends(get_current_user_from_token),
        student_service: StudentServiceInterface = Depends(Provide[Container.student_service]),
):
    if current_user.is_super_user:
        print(f"SUPERUSER ON CREATE STUDENT")
        response = await student_service.create(student=student)
        data = jsonable_encoder(response.value)
        return Response(
            content=json.dumps(data),
            media_type="application/json",
            status_code=STATUS_CODES[response.type],
        )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not permitted"
    )


@router.get("/get-by-code/")
@inject
def get_by_student_code(
        student_code: str,
        student_service: StudentServiceInterface = Depends(Provide[Container.student_service]),
):
    response = student_service.get_by_code(student_code=student_code)
    data = jsonable_encoder(response.value)
    return Response(
        content=json.dumps(data),
        media_type="application/json",
        status_code=STATUS_CODES[response.type],
    )
