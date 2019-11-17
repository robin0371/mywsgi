import contextlib

import pytest

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
