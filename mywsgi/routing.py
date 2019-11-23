"""mywsgi routing module."""
from typing import Callable, Union, Tuple

from parse import parse


class Router:
    """Router - routes requests to views."""

    views: dict  # path: view - mapping

    def __init__(self):
        self.views = {}

    def add(self, path: str) -> Callable:
        """Decorator for associate view with path."""

        def wrap(view):
            self.views[path] = view
            return view

        return wrap

    def find_view(self, path: str) -> Union[Tuple[Callable, dict], Tuple[None, None]]:
        """Return view and keywords args that associated by path."""
        for registered_path, view in self.views.items():
            parse_result = parse(registered_path, path)
            if parse_result is not None:
                return view, parse_result.named

        return None, None
