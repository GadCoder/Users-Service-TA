import contextlib
import uuid
from datetime import datetime
from typing import Any, Generator

import pytest
from fastapi import FastAPI
from sqlmodel import SQLModel
from sqlalchemy import create_engine
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from src.app.adapters.entrypoints.application import app as original_app
from tests.fake_container import Container

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="package")
def get_fake_container():
    return Container()


@pytest.fixture(scope="package")
def app():
    SQLModel.metadata.create_all(engine)
    yield original_app
    SQLModel.metadata.drop_all(engine)


@pytest.fixture
def get_student_model_dict():
    return {
        "names": "Obi Wan",
        "last_names": "Kenobi",
        "email": "obiwan.kenobi@unmsm.edu.pe",
        "picture_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRSrgDyPBG3GS6YXRsMQJmghtYYQVKa_RSk3Q&s",
        "student_code": "20200093"
    }


@pytest.fixture
def get_teacher_model_dict():
    return {
        "names": "Qui-Gon",
        "last_names": "Jinn",
        "email": "qui-gon.jinn@unmsm.edu.pe",
        "picture_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSGev6l0BBewv1l3G3PZ2g-X8D9B3oP3uiWy5tGjjmV6d36VPG6Ua4tVVeQH86wlrIrKyg&usqp=CAU",
        "teacher_code": "20200055",
        "password": "hello-there",
    }


@pytest.fixture
def get_admin_model_dict():
    return {
        "names": "Yoda",
        "last_names": "",
        "email": "yoda@unmsm.edu.pe",
        "picture_url": "https://static.wikia.nocookie.net/esstarwars/images/d/d6/Yoda_SWSB.png/revision/latest?cb=20180105191224",
        "password": "123456",
    }


@pytest.fixture(scope="module")
def client(
        app: FastAPI,
) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    with TestClient(app) as client:
        yield client
