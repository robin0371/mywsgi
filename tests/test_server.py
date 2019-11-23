import contextlib
from http import HTTPStatus

import pytest
import requests

from mywsgi.response import Response
from mywsgi.server import make_server


class TestMakeServer:
    """Tests for making server."""

    @pytest.mark.parametrize(
        "host,port,expectation",
        [
            ("localhost", 8383, contextlib.ExitStack()),
            ("127.0.0.1", 8484, contextlib.ExitStack()),
            ("localhost", "8383", pytest.raises(TypeError)),
        ],
    )
    def test_standard_usage(self, app, host, port, expectation):
        with expectation:
            server = make_server(app, host, port)

            assert server.server_address == ("127.0.0.1", port)
            assert server.app == app


class TestWSGIServer:
    def test_ok(self, app, mywsgi_server, mywsgi_addr):
        server = mywsgi_server(app)

        assert server.app is app
        assert server.server_address == mywsgi_addr

    def test_as_used_https(self, app, mywsgi_server, https_on):
        @app.router.add("/test")
        def handler(request):
            return Response(b"test!", [("Content-Type", "text/plain")])

        server = mywsgi_server(app)
        response = requests.get("http://%s:%s/test" % server.server_address)

        assert response.ok is True
        assert response.status_code == HTTPStatus.OK
        assert response.text == "test!"
