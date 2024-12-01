import json

from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, Response, HTTPException, status
from dependency_injector.wiring import Provide, inject

from src.app.domain.models.user import User
from src.app.configurator.containers import Container
from src.app.domain.ports.common.responses import ResponseTypes
from src.app.domain.ports.use_cases.user import UserServiceInterface
from src.app.adapters.entrypoints.response_status_codes import STATUS_CODES
from src.app.adapters.entrypoints.api.v1.route_login import get_current_user_from_token
from src.app.domain.schemas.user import UserCreate, UserUpdatePassword, UserUpdatePicture, \
    UserUpdateActiveStatus

router = APIRouter()


@router.post("/create/")
@inject
def create_user(
        user: UserCreate,
        current_user: User = Depends(get_current_user_from_token),
        user_service: UserServiceInterface = Depends(Provide[Container.user_service]),
):
    if current_user.is_super_user:
        response = user_service.create(user=user)
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
def get_by_user_code(
        user_code: str,
        user_service: UserServiceInterface = Depends(Provide[Container.user_service]),
):
    response = user_service.get_by_code(user_code=user_code)
    data = jsonable_encoder(response.value)
    return Response(
        content=json.dumps(data),
        media_type="application/json",
        status_code=STATUS_CODES[response.type],
    )


@router.get("/get-by-id/")
@inject
def get_by_user_id(
        id: int,
        user_service: UserServiceInterface = Depends(Provide[Container.user_service]),
):
    response = user_service.get_by_id(id=id)
    data = jsonable_encoder(response.value)
    return Response(
        content=json.dumps(data),
        media_type="application/json",
        status_code=STATUS_CODES[response.type],
    )


@router.get("/get-by-email/")
@inject
def get_by_user_email(
        user_email: str,
        user_service: UserServiceInterface = Depends(Provide[Container.user_service]),
):
    response = user_service.get_by_email(email=user_email)
    data = jsonable_encoder(response.value)
    return Response(
        content=json.dumps(data),
        media_type="application/json",
        status_code=STATUS_CODES[response.type],
    )


@router.patch("/update-password/")
@inject
def update_password(user: UserUpdatePassword,
                    current_user: User = Depends(get_current_user_from_token),
                    user_service: UserServiceInterface = Depends(Provide[Container.user_service])):
    response = user_service.update_password(user=user)
    data = jsonable_encoder(response.value)
    return Response(
        content=json.dumps(data),
        media_type="application/json",
        status_code=STATUS_CODES[response.type],
    )


@router.patch("/update-picture/")
@inject
def update_profile_picture(user: UserUpdatePicture,
                           current_user: User = Depends(get_current_user_from_token),
                           user_service: UserServiceInterface = Depends(Provide[Container.user_service])):
    if current_user.is_super_user or current_user.id == user.id:
        response = user_service.update_picture(user=user)
        data = jsonable_encoder(response.value)
        return Response(
            content=json.dumps(data),
            media_type="application/json",
            status_code=STATUS_CODES[response.type],
        )
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not permitted"
    )


@router.patch("/update-active-status/")
@inject
def update_active_status(user: UserUpdateActiveStatus,
                         current_user: User = Depends(get_current_user_from_token),
                         user_service: UserServiceInterface = Depends(Provide[Container.user_service])):
    if current_user.is_super_user:
        response = user_service.update_active_status(user=user)
        data = jsonable_encoder(response.value)
        return Response(
            content=json.dumps(data),
            media_type="application/json",
            status_code=STATUS_CODES[response.type],
        )
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not permitted"
    )


@router.delete("/delete/{id}")
@inject
def delete_by_code(id: int,
                   current_user: User = Depends(get_current_user_from_token),
                   user_service: UserServiceInterface = Depends(Provide[Container.user_service])):
    response = user_service.get_by_id(id=id)
    if response.type != ResponseTypes.SUCCESS:
        return Response(
            content=json.dumps(response.value),
            media_type="application/json",
            status_code=STATUS_CODES[response.type],
        )
    if current_user.is_super_user:
        response = user_service.delete_by_id(id_=id)
        return Response(
            content=json.dumps(response.value),
            media_type="application/json",
            status_code=STATUS_CODES[response.type],
        )
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not permitted"
    )


@router.get("/user-is-admin/{user_email}")
@inject
def user_is_admin(user_email: str,
                  user_service: UserServiceInterface = Depends(Provide[Container.user_service])):
    response = user_service.user_is_admin(user_email=user_email)
    data = jsonable_encoder(response.value)
    return Response(
        content=json.dumps(data),
        media_type="application/json",
        status_code=STATUS_CODES[response.type],
    )
