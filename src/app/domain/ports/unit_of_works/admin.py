import abc

from src.app.domain.ports.repositories.admin import AdminRepositoryInterface


class AdminUnitOfWorkInterface(abc.ABC):
    admins: AdminRepositoryInterface

    def __enter__(self) -> "AdminUnitOfWorkInterface":
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        self._commit()

    @abc.abstractmethod
    def _commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError
