from dependency_injector import containers, providers
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.app.adapters.unit_of_works.student import StudentDatabaseUnitOfWork
from src.app.adapters.use_cases.students import StudentService
from src.app.configurator import config

ENGINE = create_engine(
    config.get_database_uri()
)


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "src.app.adapters.entrypoints.api.v1",
        ]
    )

    SQLAlchemyInstrumentor().instrument(
        engine=ENGINE, enable_commenter=True, commenter_options={}
    )
    DEFAULT_SESSION_FACTORY = sessionmaker(bind=ENGINE)

    student_uow = providers.Singleton(
        StudentDatabaseUnitOfWork, session_factory=DEFAULT_SESSION_FACTORY
    )

    student_service = providers.Factory(
        StudentService,
        uow=student_uow,
    )
