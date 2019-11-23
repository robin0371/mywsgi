"""mywsgi utilities module."""
import logging
import sys

ENC, ESC = sys.getfilesystemencoding(), "surrogateescape"

LOGGER = logging.getLogger(__name__)


def unicode_to_wsgi(string):
    """Convert an environment variable to a WSGI "bytes-as-unicode" string."""
    return string.encode(ENC, ESC).decode("iso-8859-1")


def wsgi_to_bytes(string):
    """Convert string to bytes."""
    return string.encode("iso-8859-1")
