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
                    picture_url=admin_.picture_url,
                    is_superuser=admin_.is_superuser,
                    is_active=admin_.is_active
                )
                return ResponseSuccess(admin_output)
        except Exception as e:
            return ResponseFailure(ResponseTypes.SYSTEM_ERROR, e)
