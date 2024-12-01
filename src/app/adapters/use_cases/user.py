import uuid
from typing import Union

from src.app.configurator.common.hashing import Hasher
from src.app.domain.ports.common.responses import (
    ResponseFailure,
    ResponseSuccess,
    ResponseTypes,
)
from src.app.domain.models.user import User
from src.app.domain.schemas import user as user_schema
from src.app.domain.ports.use_cases.user import UserServiceInterface
from src.app.domain.ports.unit_of_works.user import UserUnitOfWorkInterface
from src.app.domain.schemas.user import UserPublic
from src.app.domain.schemas.user_base import UserLoginInput, UserLoginOutput


def _handle_response_failure(
        id: int = None, code: str = None, user_email: str = None, message: dict[str] = None
) -> ResponseFailure:
    if message:
        return ResponseFailure(ResponseTypes.RESOURCE_ERROR, message=message)
    if id:
        return ResponseFailure(
            ResponseTypes.RESOURCE_ERROR,
            message={"detail": f"User with id {id} not found"}
        )
    if code:
        return ResponseFailure(
            ResponseTypes.RESOURCE_ERROR,
            message={"detail": f"User with code code {code} not found"}
        )
    if user_email:
        return ResponseFailure(
            ResponseTypes.RESOURCE_ERROR,
            message={"detail": f"User with email {user_email} not found"}
        )


class UserService(UserServiceInterface):
    def __init__(self, uow: UserUnitOfWorkInterface):
        self.uow = uow

    def _create(
            self, user: user_schema.UserCreate
    ) -> Union[ResponseSuccess, ResponseFailure]:
        try:
            with self.uow:
                user_ = self.uow.users.get_by_code(code=user.code)
                if user_ is None:
                    hashed_password = Hasher.get_password_hash(user.password)
                    new_user = User(
                        names=user.names,
                        last_names=user.last_names,
                        email=user.email,
                        picture_url=user.picture_url,
                        code=user.code,
                        hashed_password=hashed_password,
                        is_active=True,
                        is_superuser=False
                    )
                    self.uow.users.add(new_user)
                self.uow.commit()
                user_ = user_ or self.uow.users.get_by_code(user.code)
                user_output = user_schema.UserPublic(
                    id=user_.id,
                    names=user_.names,
                    last_names=user_.last_names,
                    email=user_.email,
                    picture_url=user_.picture_url,
                    code=user_.code,
                    is_active=user_.is_active,
                    is_teacher=user_.is_teacher
                )
                return ResponseSuccess(user_output)
        except Exception as e:
            return ResponseFailure(ResponseTypes.SYSTEM_ERROR, e)

    def _get_by_id(self, id: int) -> Union[ResponseSuccess, ResponseFailure]:
        with self.uow:
            user = self.uow.users.get_by_id(id=id)
            if user:
                return ResponseSuccess(
                    UserPublic(
                        id=user.id,
                        names=user.names,
                        last_names=user.last_names,
                        email=user.email,
                        picture_url=user.picture_url,
                        code=user.code,
                        is_active=user.is_active,
                        is_teacher=user.is_teacher
                    )
                )
            return _handle_response_failure(id=id)

    def _get_by_code(self, code: str) -> Union[ResponseSuccess, ResponseFailure]:
        with self.uow:
            user = self.uow.users.get_by_code(code=code)
            if user:
                return ResponseSuccess(
                    UserPublic(
                        id=user.id,
                        names=user.names,
                        last_names=user.last_names,
                        email=user.email,
                        picture_url=user.picture_url,
                        code=user.code,
                        is_active=user.is_active,
                        is_teacher=user.is_teacher
                    )
                )
            return _handle_response_failure(code)

    def _get_by_email(self, email: str) -> Union[ResponseSuccess, ResponseFailure]:
        with self.uow:
            user = self.uow.users.get_by_email(email=email)
            if user:
                return ResponseSuccess(
                    UserPublic(
                        id=user.id,
                        names=user.names,
                        last_names=user.last_names,
                        email=user.email,
                        picture_url=user.picture_url,
                        code=user.code,
                        is_active=user.is_active,
                        is_superuser=user.is_superuser
                    )
                )
            return _handle_response_failure(email=email)

    def _update_password(self, user: user_schema.UserUpdatePassword) -> Union[
        ResponseSuccess, ResponseFailure]:
        with self.uow:
            user_ = self.uow.users.get_by_id(id=user.id)
            if not user:
                return _handle_response_failure(user.id)
            if not Hasher.verify_password(user.existing_password, user_.hashed_password):
                return _handle_response_failure(message="The existing password is incorrect")
            new_hashed_password = Hasher.get_password_hash(user.new_password)
            user_.hashed_password = new_hashed_password
            self.uow.commit()
            user_output = user_schema.UserPublic(
                id=user_.id,
                names=user_.names,
                last_names=user_.last_names,
                email=user_.email,
                picture_url=user_.picture_url,
                code=user_.code,
                is_active=user_.is_active,
                is_teacher=user_.is_teacher
            )
            return ResponseSuccess(user_output)

    def _update_picture(self, user: user_schema.UserUpdatePicture) -> Union[ResponseSuccess, ResponseFailure]:
        with self.uow:
            user_ = self.uow.users.get_by_id(id=user.id)
            if not user_:
                return _handle_response_failure(user.code)
            user_.picture_url = user.picture_url
            self.uow.commit()
            user_output = user_schema.UserPublic(
                id=user_.id,
                names=user_.names,
                last_names=user_.last_names,
                email=user_.email,
                picture_url=user_.picture_url,
                code=user_.code,
                is_active=user_.is_active,
                is_teacher=user_.is_teacher
            )
            return ResponseSuccess(user_output)

    def _update_active_status(self, user: user_schema.UserUpdateActiveStatus) -> Union[
        ResponseSuccess, ResponseFailure]:
        with self.uow:
            user_ = self.uow.users.get_by_id(id=user.id)
            if not user_:
                return _handle_response_failure(user.code)
            user_.is_active = user.is_active
            self.uow.commit()
            user_output = user_schema.UserPublic(
                id=user_.id,
                names=user_.names,
                last_names=user_.last_names,
                email=user_.email,
                picture_url=user_.picture_url,
                code=user_.code,
                is_active=user_.is_active,
                is_teacher=user_.is_teacher

            )
            return ResponseSuccess(user_output)

    def _delete_by_code(self, code: str) -> Union[
        ResponseSuccess, ResponseFailure]:
        with self.uow:
            existing_user = self.uow.users.get_by_code(code=code)
            if not existing_user:
                return _handle_response_failure(code)
            self.uow.session.delete(existing_user)
            self.uow.commit()
            return ResponseSuccess(value={"detail": "User deleted successfully"})

    def _delete_by_id(self, id: int) -> Union[
        ResponseSuccess, ResponseFailure]:
        with self.uow:
            existing_user = self.uow.users.get_by_id(id=id)
            if not existing_user:
                return _handle_response_failure(id)
            self.uow.session.delete(existing_user)
            self.uow.commit()
            return ResponseSuccess(value={"detail": f"User with id {id}deleted successfully"})

    def _authenticate_user(self, user: UserLoginInput) -> Union[UserLoginOutput, bool]:
        with self.uow:
            user_ = self.uow.users.get_by_email(user.email)
            if not user_ or not Hasher.verify_password(
                    user.password, user_.hashed_password
            ):
                return False
            return UserLoginOutput(
                id=user_.id,
                user_name=user_.names,
                email=user_.email,
                is_active=user_.is_active,
                is_super_user=user_.is_superuser,
            )
