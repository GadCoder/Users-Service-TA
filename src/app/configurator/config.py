import os
from pathlib import Path

from dotenv import load_dotenv

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    PROJECT_NAME: str = "Tutoring Platform - Users Microservice"
    PROJECT_VERSION: str = "1.0.0"

    USE_SQLITE_DB: bool = os.getenv("USE_SQLITE_DB")
    MYSQL_USER: str = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_SERVER: str = os.getenv("MYSQL_SERVER", "localhost")
    MYSQL_PORT: str = os.getenv(
        "MYSQL_PORT", 3306
    )  # default MYSQL port is 3306
    MYSQL_DB: str = os.getenv("MYSQL_DB", "tdd")
    DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_SERVER}:{MYSQL_PORT}/{MYSQL_DB}"

    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30  # in mins

    TEST_USER_EMAIL = "obiwan@kenobi.com"


settings = Settings()


def get_database_uri() -> str:
    print(f"USE_SQLITE_DB: {settings.USE_SQLITE_DB}")
    print(f"MYSQL_HOST: {settings.MYSQL_SERVER}")
    if settings.USE_SQLITE_DB:
        return "sqlite:///./sql_app.db"
    return settings.DATABASE_URL
