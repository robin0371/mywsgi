"""mywsgi - server/gateway module."""
import os
import sys
import logging

from http.server import (
    HTTPServer as BaseHTTPServer,
    BaseHTTPRequestHandler,
)
from typing import Type

from mywsgi.base import HeadersType

ENC, ESC = sys.getfilesystemencoding(), "surrogateescape"

LOGGER = logging.getLogger(__name__)


def unicode_to_wsgi(string):
    """Convert an environment variable to a WSGI "bytes-as-unicode" string."""
    return string.encode(ENC, ESC).decode("iso-8859-1")


def wsgi_to_bytes(string):
    """Convert string to bytes."""
    return string.encode("iso-8859-1")


def get_env() -> dict:
    """Return environment variables."""
    env = {k: unicode_to_wsgi(v) for k, v in os.environ.items()}
    env["wsgi.input"] = sys.stdin.buffer
    env["wsgi.errors"] = sys.stderr
    env["wsgi.version"] = (1, 0)
    env["wsgi.multithread"] = False
    env["wsgi.multiprocess"] = False
    env["wsgi.run_once"] = True

    if env.get("HTTPS", "off") in ("on", "1"):
        env["wsgi.url_scheme"] = "https"
    else:
        env["wsgi.url_scheme"] = "http"

    return env


class WSGIRequestHandler(BaseHTTPRequestHandler):
    """WSGI request handler."""

    def handle_one_request(self):
        env = get_env()
        headers_set, headers_sent = [], []

        def write(body: bytes):
            if not headers_set:
                raise AssertionError("write() before start_response()")

            out = self.wfile
            http_headers = b""

            if not headers_sent:
                # Before the first output, send the stored headers
                status, response_headers = headers_sent[:] = headers_set
                head = f"HTTP/1.1 {status}"
                headers = "".join([f"{h[0]}: {h[1]}\r\n" for h in response_headers])
                http_data = f"{head}\r\n{headers}\r\n"
                http_headers = wsgi_to_bytes("".join(http_data))

            http_result = http_headers + body
            LOGGER.debug("http response=%s", http_result)
            out.write(http_result)
            out.flush()

        def start_response(status: str, response_headers: HeadersType, exc_info=None):
            if exc_info:
                try:
                    if headers_sent:
                        # Re-raise original exception if headers sent
                        raise exc_info[1].with_traceback(exc_info[2])
                finally:
                    exc_info = None  # avoid dangling circular ref
            elif headers_set:
                raise AssertionError("Headers already set!")

            headers_set[:] = [status, response_headers]

            return write

        result = self.server.app(env, start_response)

        try:
            for data in result:
                if data:  # don't send headers until body appears
                    write(data)
            if not headers_sent:
                write(b"")  # send headers now if body was empty
        finally:
            if hasattr(result, "close"):
                result.close()


class WSGIServer(BaseHTTPServer):
    """WSGI server."""

    def __init__(self, host: str, port: int, app, handler: Type[WSGIRequestHandler]):
        super(WSGIServer, self).__init__((host, port), handler)
        self.app = app


def make_server(app, host: str, port: int) -> WSGIServer:
    """Return WSGI server."""
    server = WSGIServer(host, port, app, WSGIRequestHandler)
    return server
