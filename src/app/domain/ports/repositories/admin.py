import abc
import uuid

from src.app.domain.schemas import admin as admin_schema


class AdminRepositoryInterface(abc.ABC):
    def __init__(self):
        self.seen = set()

    def add(self, admin: admin_schema.AdminCreate):
        self._add(admin)
        self.seen.add(hash(admin.admin_code))

    def get_by_code(self, admin_code: uuid.UUID) -> admin_schema.AdminPublic:
        admin = self._get_by_code(admin_code=admin_code)
        if admin:
            self.seen.add(hash(admin.admin_code))
        return admin

    def get_by_email(self, email: str) -> admin_schema.AdminPublic:
        admin = self._get_by_email(email=email)
        if admin:
            self.seen.add(hash(admin.admin_code))
        return admin

    @abc.abstractmethod
    def _add(self, admin: admin_schema.AdminCreate):
        raise NotImplementedError

    @abc.abstractmethod
    def _get_by_code(self, admin_code: uuid.UUID) -> admin_schema.AdminPublic:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_by_email(self, email: str) -> admin_schema.AdminPublic:
        raise NotImplementedError
