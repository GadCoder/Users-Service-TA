from typing import Any, Callable

from sqlalchemy.orm import Session

from src.app.adapters.repositories.user import UserDatabaseRepository
from src.app.domain.ports.unit_of_works.user import UserUnitOfWorkInterface


class UserDatabaseUnitOfWork(UserUnitOfWorkInterface):
    def __init__(self, session_factory: Callable[[], Any]):
        self.session_factory = session_factory()

    def __enter__(self):
        self.session: Session = self.session_factory()
        self.users = UserDatabaseRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def _commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
