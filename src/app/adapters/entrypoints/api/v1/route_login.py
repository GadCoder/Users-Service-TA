from datetime import timedelta

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt

from src.app.adapters.entrypoints.api.utils import OAuth2PasswordBearerWithCookie
from src.app.configurator.common.security import create_access_token
from src.app.configurator.config import settings
from src.app.configurator.containers import Container
from src.app.domain.ports.use_cases.user import UserServiceInterface
from src.app.domain.schemas.tokens import Token
from src.app.domain.schemas.user_base import UserLoginInput, UserLoginOutput

router = APIRouter()


@router.post("/token", response_model=Token)
@inject
def login_for_access_token(
        response: Response,
        form_data: OAuth2PasswordRequestForm = Depends(),
        user_service: UserServiceInterface = Depends(Provide[Container.user_service]),
):
    user = UserLoginInput(email=form_data.username, password=form_data.password)
    user = user_service.authenticate_user(user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    response.set_cookie(
        key="access_token", value=f"Bearer {access_token}", httponly=True
    )
    return {"access_token": access_token, "token_type": "bearer"}


oauth2_scheme = OAuth2PasswordBearerWithCookie(token_url="/login/token")


@inject
def get_current_user_from_token(
        token: str = Depends(oauth2_scheme),
        user_service: UserServiceInterface = Depends(Provide[Container.user_service]),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_name: str = payload.get("sub")
        print("username/email extracted is ", user_name)
        if user_name is None:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception from e
    with user_service.uow:
        user = user_service.uow.users.get_by_email(user_name)
        if user is None:
            raise credentials_exception
        return UserLoginOutput(
            id=user.id,
            user_name=user.names,
            email=user.email,
            is_active=user.is_active,
            is_super_user=user.is_superuser,
        )
