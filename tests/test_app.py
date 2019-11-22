import contextlib

import pytest

from mywsgi.app import Application, import_app


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
