import importlib
import sys

import pytest

from mywsgi.app import Application


@pytest.fixture
def app():
    """Returns initialized WSGI application."""
    return Application()


@pytest.fixture
def new_py_module():
    """Returns function for creating new python module from string."""
    module_name = "my_test_mywsgi_module"

    def _new_module(code="from mywsgi import App\napp = App()"):
        """Returns registered module with custom code.

        By default: creates module with initialized WSGI application.
        """
        spec = importlib.util.spec_from_loader(module_name, loader=None)
        module = importlib.util.module_from_spec(spec)
        exec(code, module.__dict__)
        sys.modules[module_name] = module
        return module

    yield _new_module
    del sys.modules[module_name]
