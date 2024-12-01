import abc

from src.app.domain.schemas import user as user_schema


class UserRepositoryInterface(abc.ABC):
    def __init__(self):
        self.seen = set()

    def add(self, user: user_schema.UserCreate):
        self._add(user)
        self.seen.add(hash(user.code))

    def get_by_id(self, id: int) -> user_schema.UserPublic:
        user = self._get_by_id(id)
        if user:
            self.seen.add(hash(user.code))
        return user

    def get_by_code(self, code: str) -> user_schema.UserPublic:
        user = self._get_by_code(code)
        if user:
            self.seen.add(hash(user.code))
        return user

    def get_by_email(self, email: str) -> user_schema.UserPublic:
        user = self._get_by_email(email)
        if user:
            self.seen.add(hash(user.code))
        return user

    @abc.abstractmethod
    def _add(self, user: user_schema.UserCreate):
        raise NotImplementedError

    @abc.abstractmethod
    def _get_by_code(self, code: str) -> user_schema.UserPublic:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_by_id(self, id: int) -> user_schema.UserPublic:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_by_email(self, email: str) -> user_schema.UserPublic:
        raise NotImplementedError
