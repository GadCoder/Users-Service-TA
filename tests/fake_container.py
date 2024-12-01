from dependency_injector import containers, providers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.app.adapters.use_cases.admin import AdminService
from src.app.adapters.use_cases.student import StudentService
from src.app.adapters.use_cases.teacher import TeacherService
from src.app.adapters.unit_of_works.admin import AdminDatabaseUnitOfWork
from src.app.adapters.unit_of_works.student import StudentDatabaseUnitOfWork
from src.app.adapters.unit_of_works.teacher import TeacherDatabaseUnitOfWork


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
    teacher_uow = providers.Singleton(
        TeacherDatabaseUnitOfWork, session_factory=DEFAULT_SESSION_FACTORY
    )
    admin_uow = providers.Singleton(
        AdminDatabaseUnitOfWork, session_factory=DEFAULT_SESSION_FACTORY
    )
    fake_student_service = providers.Factory(
        StudentService,
        uow=student_uow,
    )
    fake_teacher_service = providers.Factory(
        TeacherService,
        uow=teacher_uow,
    )
    fake_admin_service = providers.Factory(
        AdminService,
        uow=admin_uow
    )
