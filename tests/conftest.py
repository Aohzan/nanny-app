"""App for tests."""

import pytest
from flask import Flask
from flask.testing import FlaskClient

from app.app import create_app


@pytest.fixture()
def app():
    app = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "03692235214508620010da81e406b5766db9e61b650bb9f9ab61ed134ec742c3",
            "WTF_CSRF_ENABLED": False,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///tests.db",
        }
    )
    app.testing = True

    yield app


@pytest.fixture()
def client(app: Flask) -> FlaskClient:
    return app.test_client()
