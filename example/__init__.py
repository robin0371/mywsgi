"""Demo application."""
from mywsgi import App
from mywsgi.response import Response
from mywsgi.util import wsgi_to_bytes

app = App()


@app.router.add("/")
def index(request):
    return Response(b"index", [("Content-Type", "text/plain")])


@app.router.add("/get/{param}")
def get_named_param(request, param):
    return Response(wsgi_to_bytes(f"{param}"), [("Content-Type", "text/plain")])


@app.router.add("/json/{param}")
def get_json(request, param):
    return Response(wsgi_to_bytes('{"p": %s}' % param), [("Content-Type", "application/json")])
