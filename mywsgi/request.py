"""mywsgi - requests module."""
from mywsgi.base import EnvType


class Request:
    """Request object represents each request to the app."""

    def __init__(self, env: EnvType):
        self.env = env
