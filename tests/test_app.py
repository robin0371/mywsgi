import contextlib
from http import HTTPStatus

import pytest
import requests

from mywsgi.app import Application, import_app
from mywsgi.response import Response
from mywsgi.util import wsgi_to_bytes


class TestImportApp:
    """Tests for import application."""

    @pytest.mark.parametrize(
        "code,expectation",
        [
            ("from mywsgi import App\napp = App()", contextlib.ExitStack()),
            ("from mywsgi import App\napp = App", pytest.raises(AssertionError)),
            ("from mywsgi import App\napp2 = App()", pytest.raises(AssertionError)),
            ("from mywsgi import App", pytest.raises(AssertionError)),
            ("", pytest.raises(AssertionError)),
        ],
    )
    def test_module_content(self, new_py_module, code, expectation):
        module = new_py_module(code)

        with expectation:
            app = import_app(f"{module.__name__}:app")
            assert isinstance(app, Application)

    @pytest.mark.parametrize(
        "app_ref,expectation",
        [
            ("my_test_mywsgi_module:app", contextlib.ExitStack()),
            ("my_test:app", pytest.raises(ModuleNotFoundError)),
            ("my_test_mywsgi_module:", pytest.raises(AssertionError)),
            ("my_test_mywsgi_module:app2", pytest.raises(AssertionError)),
            ("my_test_mywsgi_module!app", pytest.raises(ValueError)),
            (":app", pytest.raises(ValueError)),
            ("", pytest.raises(ValueError)),
        ],
    )
    def test_input_app_reference(self, new_py_module, app_ref, expectation):
        new_py_module()

        with expectation:
            app = import_app(app_ref)
            assert isinstance(app, Application)


class TestRouting:
    def test_few_routes(self, app, mywsgi_server):
        @app.router.add("/a")
        def handler_a(request):
            return Response(b"a!", [("Content-Type", "text/plain")])

        @app.router.add("/b")
        def handler_b(request):
            return Response(b"b!", [("Content-Type", "text/plain")])

        server = mywsgi_server(app)

        response_a = requests.get("http://%s:%s/a" % server.server_address)

        assert response_a.ok is True
        assert response_a.status_code == HTTPStatus.OK
        assert response_a.text == "a!"

        response_b = requests.get("http://%s:%s/b" % server.server_address)

        assert response_b.ok is True
        assert response_b.status_code == HTTPStatus.OK
        assert response_b.text == "b!"

    def test_named_params(self, app, mywsgi_server):
        @app.router.add("/test/{number}")
        def handler(request, number):
            return Response(
                wsgi_to_bytes(f"{number}!"), [("Content-Type", "text/plain")]
            )

        server = mywsgi_server(app)

        response = requests.get("http://%s:%s/test/123" % server.server_address)

        assert response.ok is True
        assert response.status_code == HTTPStatus.OK
        assert response.text == "123!"

    def test_route_does_not_exist(self, app, mywsgi_server):
        @app.router.add("/test")
        def handler(request):
            return Response(b"test!", [("Content-Type", "text/plain")])

        server = mywsgi_server(app)
        response = requests.get("http://%s:%s/not-existed" % server.server_address)

        assert response.ok is False
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.text == "Bad Request"


class TestHeaders:
    def test_ok(self, mocker, app, mywsgi_server):
        mocker.patch(
            "mywsgi.server.BaseHTTPRequestHandler.date_time_string",
            return_value="Sat, 23 Nov 2019 17:42:54 GMT",
        )

        @app.router.add("/test")
        def handler(request):
            return Response(b"test!", [("Content-Type", "text/plain")])

        server = mywsgi_server(app)
        response = requests.get("http://%s:%s/test" % server.server_address)

        assert response.ok is True
        assert response.status_code == HTTPStatus.OK
        assert response.text == "test!"
        assert response.headers["content-type"] == "text/plain"
        assert response.headers["content-length"] == "5"
        assert response.headers["date"] == "Sat, 23 Nov 2019 17:42:54 GMT"
