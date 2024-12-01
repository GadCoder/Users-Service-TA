import abc
import uuid
from typing import Union

from src.app.domain.schemas import admin as admin_schema
from src.app.domain.ports.unit_of_works.admin import AdminUnitOfWorkInterface
from src.app.domain.ports.common.responses import ResponseFailure, ResponseSuccess


class AdminServiceInterface(abc.ABC):
    @abc.abstractmethod
    def __init__(self, uow: AdminUnitOfWorkInterface):
        self.uow = uow

    def create(self, admin: admin_schema.AdminCreate) -> Union[ResponseSuccess, ResponseFailure]:
        return self._create(admin)

    def get_by_code(self, admin_code: uuid.UUID) -> Union[ResponseSuccess, ResponseFailure]:
        return self._get_by_code(admin_code)

    def get_by_email(self, email: str) -> Union[ResponseSuccess, ResponseFailure]:
        return self._get_by_email(email)

    @abc.abstractmethod
    def _create(
            self, user: admin_schema.AdminCreate
    ) -> Union[ResponseSuccess, ResponseFailure]:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_by_code(self, admin_code: uuid.UUID) -> Union[ResponseSuccess, ResponseFailure]:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_by_email(self, email: str) -> Union[ResponseSuccess, ResponseFailure]:
        raise NotImplementedError
