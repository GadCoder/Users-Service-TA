import uuid

from src.app.domain.models.admin import Admin
from src.app.domain.schemas import admin as admin_schema
from src.app.domain.ports.repositories.admin import AdminRepositoryInterface


class AdminDatabaseRepository(AdminRepositoryInterface):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def _add(self, admin):
        self.session.add(admin)

    def _get_by_code(self, admin_code: uuid.UUID) -> admin_schema.AdminPublic:
        return self.session.query(Admin).filter(Admin.admin_code == admin_code).first()

    def _get_by_email(self, email: str) -> admin_schema.AdminPublic:
        return self.session.query(Admin).filter(Admin.email == email).first()
