import abc
from typing import Union

from src.app.domain.schemas import user as user_schema
from src.app.domain.ports.unit_of_works.user import UserUnitOfWorkInterface
from src.app.domain.ports.common.responses import ResponseFailure, ResponseSuccess
from src.app.domain.schemas.user_base import UserLoginInput, UserLoginOutput


class UserServiceInterface(abc.ABC):
    @abc.abstractmethod
    def __init__(self, uow: UserUnitOfWorkInterface):
        self.uow = uow

    def create(self, user: user_schema.UserCreate) -> Union[ResponseSuccess, ResponseFailure]:
        return self._create(user)

    def get_by_id(self, id: int) -> Union[ResponseSuccess, ResponseFailure]:
        return self._get_by_id(id)

    def get_by_code(self, user_code: str) -> Union[ResponseSuccess, ResponseFailure]:
        return self._get_by_code(user_code)

    def get_by_email(self, email: str) -> Union[ResponseSuccess, ResponseFailure]:
        return self._get_by_email(email)

    def update_picture(self, user: user_schema.UserUpdatePicture) -> Union[ResponseSuccess, ResponseFailure]:
        return self._update_picture(user)

    def update_password(self, user: user_schema.UserUpdatePassword) -> Union[ResponseSuccess, ResponseFailure]:
        return self._update_password(user)

    def update_active_status(self, user: user_schema.UserUpdateActiveStatus) -> Union[
        ResponseSuccess, ResponseFailure]:
        return self._update_active_status(user)

    def delete_by_id(self, id: int) -> Union[
        ResponseSuccess, ResponseFailure]:
        return self._delete_by_id(id)

    def delete_by_code(self, user_code: str) -> Union[
        ResponseSuccess, ResponseFailure]:
        return self._delete_by_code(user_code)

    def authenticate_user(self, user: UserLoginInput) -> Union[UserLoginOutput, bool]:
        return self._authenticate_user(user)

    def user_is_admin(self, user_email: str) -> Union[ResponseSuccess, ResponseFailure]:
        return self._user_is_admin(user_email)

    @abc.abstractmethod
    def _create(
            self, user: user_schema.UserCreate
    ) -> Union[ResponseSuccess, ResponseFailure]:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_by_code(self, user_code: str) -> Union[ResponseSuccess, ResponseFailure]:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_by_id(self, id: int) -> Union[ResponseSuccess, ResponseFailure]:
        raise NotImplementedError

    @abc.abstractmethod
    def _update_picture(self, user: user_schema.UserCreate) -> Union[ResponseSuccess, ResponseFailure]:
        raise NotImplementedError

    @abc.abstractmethod
    def _update_password(self, user: user_schema.UserCreate) -> Union[ResponseSuccess, ResponseFailure]:
        raise NotImplementedError

    @abc.abstractmethod
    def _update_active_status(self, user: user_schema.UserUpdateActiveStatus) -> Union[
        ResponseSuccess, ResponseFailure]:
        raise NotImplementedError

    @abc.abstractmethod
    def _delete_by_code(self, user_code: str) -> Union[
        ResponseSuccess, ResponseFailure]:
        raise NotImplementedError

    @abc.abstractmethod
    def _delete_by_id(self, id: int) -> Union[
        ResponseSuccess, ResponseFailure]:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_by_email(self, email: str) -> Union[ResponseSuccess, ResponseFailure]:
        raise NotImplementedError

    @abc.abstractmethod
    def _authenticate_user(self, user: UserLoginInput) -> Union[UserLoginOutput, bool]:
        raise NotImplementedError

    @abc.abstractmethod
    def _user_is_admin(self, user_email: str) -> Union[ResponseSuccess, ResponseFailure]:
        raise NotImplementedError
