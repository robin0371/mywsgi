import pytest

from mywsgi.routing import Router


def view():
    pass


class TestRouter:

    def test_adding(self):
        router = Router()

        @router.add("/path-a")
        def func_a():
            pass

        @router.add("/path-b")
        def func_b():
            pass

        assert router.views["/path-a"] is func_a
        assert router.views["/path-b"] is func_b

    @pytest.mark.parametrize(
        "registered_path,requested_path,expectation",
        [
            ("/test", "/test", (view, {})),
            ("/test/{number}", "/test/123", (view, {"number": "123"})),
            ("/test/{a}/{b}", "/test/a/2", (view, {"a": "a", "b": "2"})),
            ("/tree/{tree_id}/id/{id}", "/tree/1/id/2", (view, {"tree_id": "1", "id": "2"})),
        ],
    )
    def test_find_view(self, registered_path, requested_path, expectation):
        global view

        router = Router()
        router.add(registered_path)(view)

        assert router.views[registered_path] is view
        assert router.find_view(requested_path) == expectation
