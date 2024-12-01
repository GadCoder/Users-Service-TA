from src.app.domain.models.user import User
from src.app.domain.schemas import user as user_schema
from src.app.domain.ports.repositories.user import UserRepositoryInterface


class UserDatabaseRepository(UserRepositoryInterface):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def _add(self, user):
        self.session.add(user)

    def _get_by_id(self, id: int) -> user_schema.UserPublic:
        return self.session.get(User, id)

    def _get_by_code(self, code: str) -> user_schema.UserPublic:
        return self.session.query(User).filter(User.code == code).first()

    def _get_by_email(self, email: str) -> user_schema.UserPublic:
        return self.session.query(User).filter(User.email == email).first()
