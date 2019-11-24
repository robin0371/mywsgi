"""mywsgi - application/framework module."""
import importlib
import logging

from mywsgi.base import BodyType, EnvType, StartRespType
from mywsgi.request import Request
from mywsgi.response import Response
from mywsgi.routing import Router

LOGGER = logging.getLogger(__name__)


class Application:
    """WSGI-compatible application."""

    def __init__(self):
        self.router = Router()

    def __call__(self, env: EnvType, start_response: StartRespType) -> BodyType:
        request = Request(env)

        response = self.handle_request(request)

        return response(env, start_response)

    def handle_request(self, request: Request) -> Response:
        """Handle request."""
        query = request.env.get("QUERY_STRING")
        view, kwargs = self.router.find_view(query)

        if view:
            LOGGER.info("view=%s kwargs=%s", repr(view), kwargs)
            response = view(request, **kwargs)
        else:
            LOGGER.info("view associated with %s doesn't exist", query)
            response = Response(
                b"Bad Request", [("Content-Type", "text/plain")], "400 Bad Request"
            )

        return response


def import_app(app_reference: str) -> Application:
    """Returns application by reference."""
    module_reference, app_name = app_reference.split(":")
    app_module = importlib.import_module(module_reference)
    app = getattr(app_module, app_name, None)

    assert isinstance(app, Application), f"app should be instance of {repr(Application)}"

    return app
