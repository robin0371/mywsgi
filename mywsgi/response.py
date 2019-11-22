"""mywsgi - responses module."""
from mywsgi.base import BodyType, ByteString, EnvType, HeadersType, StartRespType


class Response:
    """Response object represents each response from the app."""

    def __init__(self, body: ByteString, headers: HeadersType, status: str = "200 OK"):
        self.status = status
        self.headers = headers
        self.body = body

        self.add_content_length()

    def __call__(self, env: EnvType, start_response: StartRespType) -> BodyType:
        start_response(self.status, self.headers)
        return [self.body]

    def add_content_length(self):
        """Calculate content length and add it to the headers."""
        self.headers.append(("Content-Length", str(len(self.body))))
