import os
import sys
from typing import Any, Generator

import pytest
from routing.base import api_router
from core.config import settings
from db.base import Base
from db.session import get_db
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from tests.utils import authentication_token_from_email

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def start_application():
    """
    Function to start the application and return a FastAPI instance.
    """
    app = FastAPI()
    app.include_router(api_router)
    return app


@pytest.fixture(scope="module", name="app")
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """
    Base.metadata.create_all(engine)
    _app = start_application()
    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="module")
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    """
    Fixture function that returns a database session for testing purposes.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        Generator[SessionTesting, Any, None]: A generator that yields a testing session for database operations.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="module", name="client")
def client(
    app: FastAPI, db_session: SessionTesting
) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, db_session: Session):
    """
    Fixture to generate token headers for a normal user using the provided TestClient and Session.

    Parameters:
    - client: TestClient object
    - db_session: Session object

    Returns:
    - Authentication token generated from the email of the test user specified in the settings
    """
    return authentication_token_from_email(
        client=client, email=settings.TEST_USER_EMAIL, db=db_session
    )