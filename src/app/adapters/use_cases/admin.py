import uuid
from typing import Union

from src.app.domain.ports.common.responses import (
    ResponseFailure,
    ResponseSuccess,
    ResponseTypes,
)

from src.app.domain.models.admin import Admin
from src.app.domain.schemas import admin as admin_schema
from src.app.domain.ports.use_cases.admin import AdminServiceInterface
from src.app.domain.ports.unit_of_works.admin import AdminUnitOfWorkInterface
from src.app.domain.schemas.admin import AdminPublic


def _handle_response_failure(
        admin_code: uuid.UUID = None, admin_email: str = None, message: dict[str] = None
) -> ResponseFailure:
    if message:
        return ResponseFailure(ResponseTypes.RESOURCE_ERROR, message=message)
    if admin_code and not admin_email:
        return ResponseFailure(
            ResponseTypes.RESOURCE_ERROR,
            message={"detail": f"Admin with code code {admin_code} not found"}
        )
    if admin_email and not admin_code:
        return ResponseFailure(
            ResponseTypes.RESOURCE_ERROR,
            message={"detail": f"Admin with email {admin_email} not found"}
        )


class AdminService(AdminServiceInterface):
    def __init__(self, uow: AdminUnitOfWorkInterface):
        self.uow = uow

    def _create(
            self, admin: admin_schema.AdminCreate) -> Union[ResponseSuccess, ResponseFailure]:
        try:
            with self.uow:
                admin_ = self.uow.admins.get_by_email(email=admin.email)
                if admin_ is None:
                    new_admin = Admin(
                        names=admin.names,
                        last_names=admin.last_names,
                        email=admin.email,
                        password=admin.password,
                    )
                    self.uow.admins.add(new_admin)
                self.uow.commit()
                admin_ = admin_ or self.uow.admins.get_by_email(email=admin.email)
                admin_output = admin_schema.AdminPublic(
                    id=admin_.id,
                    names=admin_.names,
                    last_names=admin_.last_names,
                    email=admin_.email,
                    admin_code=admin_.admin_code,
                    picture_url=admin_.picture_url,
                    is_superuser=admin_.is_superuser,
                    is_active=admin_.is_active
                )
                return ResponseSuccess(admin_output)
        except Exception as e:
            return ResponseFailure(ResponseTypes.SYSTEM_ERROR, e)

    def _get_by_code(self, admin_code: uuid.UUID) -> Union[ResponseSuccess, ResponseFailure]:
        with self.uow:
            admin = self.uow.admins.get_by_code(admin_code=admin_code)
            if admin:
                return ResponseSuccess(
                    AdminPublic(
                        id=admin.id,
                        names=admin.names,
                        last_names=admin.last_names,
                        email=admin.email,
                        picture_url=admin.picture_url,
                        admin_code=admin.admin_code,
                        is_active=admin.is_active,
                        is_superuser=admin.is_superuser
                    )
                )
            return _handle_response_failure(admin_code=admin_code)

    def _get_by_email(self, email: str) -> Union[ResponseSuccess, ResponseFailure]:
        with self.uow:
            admin = self.uow.admins.get_by_email(email=email)
            if admin:
                return ResponseSuccess(
                    AdminPublic(
                        id=admin.id,
                        names=admin.names,
                        last_names=admin.last_names,
                        email=admin.email,
                        picture_url=admin.picture_url,
                        admin_code=admin.admin_code,
                        is_active=admin.is_active,
                        is_superuser=admin.is_superuser
                    )
                )
            return _handle_response_failure(email=email)
