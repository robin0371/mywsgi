import contextlib
from http import HTTPStatus

import pytest
import requests

from mywsgi.app import Application, import_app
from mywsgi.response import Response


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
