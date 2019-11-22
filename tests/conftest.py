import importlib
import sys
import threading

import pytest

from mywsgi.app import Application
from mywsgi.server import make_server


class WSGIServerWrapper:
    """Wrapper for simple start/stop mywsgi server in thread."""

    def __init__(self, server):
        self.server = server
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)

    def start(self):
        self.thread.start()

    def stop(self):
        self.server._BaseServer__is_shut_down.set()  # noqa
        self.server.shutdown()

        stop_threads = True  # noqa
        self.thread.join()


@pytest.fixture
def app():
    """Returns initialized WSGI application."""
    return Application()


@pytest.fixture
def mywsgi_addr():
    """Returns mywsgi test server (host, port)."""
    return "127.0.0.1", 8089


@pytest.fixture
def mywsgi_server(mywsgi_addr):
    """Returns function for creating mywsgi server."""
    data = {}

    def start_server(app):
        server = make_server(app, *mywsgi_addr)
        server_wrapper = WSGIServerWrapper(server)
        data["server"] = server_wrapper
        server_wrapper.start()
        return server

    yield start_server

    data["server"].stop()


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
