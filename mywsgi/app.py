"""mywsgi - application/framework module."""
import importlib

from mywsgi.base import BodyType, EnvType, StartRespType
from mywsgi.request import Request
from mywsgi.response import Response


class Application:
    """WSGI-compatible application."""

    def __call__(self, env: EnvType, start_response: StartRespType) -> BodyType:
        request = Request(env)
        response = self.handle_request(request)
        return response(env, start_response)

    def handle_request(self, request: Request) -> Response:
        """Handle request."""
        body = b"Hello!!"
        response = Response(body, [("Content-Type", "text/plain")])
        return response


def import_app(app_reference: str) -> Application:
    """Returns application by reference."""
    module_reference, app_name = app_reference.split(":")
    app_module = importlib.import_module(module_reference)
    app = getattr(app_module, app_name, None)

    assert isinstance(app, Application), f"app should be instance of {repr(Application)}"

    return app
