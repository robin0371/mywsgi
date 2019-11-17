"""mywsgi - launcher module."""
import logging

import click

from mywsgi.app import import_app
from mywsgi.server import make_server

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s:%(lineno)d %(levelname)s %(message)s",
    handlers=[logging.StreamHandler()],
)

LOGGER = logging.getLogger(__name__)


@click.command()
@click.argument("app_reference")
@click.argument("host", default="localhost")
@click.argument("port", default=8080, type=int)
def main(app_reference="", host="", port=0):
    """Launch WSGI-server with application."""
    LOGGER.info("start mywsgi...")

    try:
        LOGGER.info("app config reference=%s", app_reference)
        app = import_app(app_reference)

        LOGGER.info("server config host=%s port=%s", host, port)
        server = make_server(app, host, port)

        LOGGER.info("mywsgi start serving...")
        server.serve_forever()
    except Exception:
        LOGGER.exception("an error has occurred")
    finally:
        LOGGER.info("mywsgi stopped.")


if __name__ == "__main__":
    main()
