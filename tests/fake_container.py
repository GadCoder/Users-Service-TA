from dependency_injector import containers, providers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.app.adapters.use_cases.student import StudentService
from src.app.adapters.use_cases.user import UserService
from src.app.adapters.unit_of_works.student import StudentDatabaseUnitOfWork
from src.app.adapters.unit_of_works.user import UserDatabaseUnitOfWork


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "src.app.adapters.entrypoints.api.v1",
            "tests"
        ]
    )

    DEFAULT_SESSION_FACTORY = lambda: sessionmaker(
        bind=create_engine(
            "sqlite:///./test_db.db", connect_args={"check_same_thread": False}
        )
    )

    student_uow = providers.Singleton(
        StudentDatabaseUnitOfWork, session_factory=DEFAULT_SESSION_FACTORY
    )
    user_uow = providers.Singleton(
        UserDatabaseUnitOfWork, session_factory=DEFAULT_SESSION_FACTORY
    )

    fake_student_service = providers.Factory(
        StudentService,
        uow=student_uow,
    )
    fake_user_service = providers.Factory(
        UserService,
        uow=user_uow,
    )
