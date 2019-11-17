import pytest

from mywsgi.app import Application


@pytest.fixture
def app():
    """Returns initialized WSGI application."""
    return Application()
