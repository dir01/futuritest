from random import randint
from wsgiref.simple_server import make_server

from pyramid.config import Configurator
from pyramid.response import Response
from utils import generate_random_string


def hello_world(request):
    response_length = randint(0, 9000)
    response = generate_random_string(response_length)
    return Response(response)


def main():
    config = Configurator()
    config.add_route('any', '*url')
    config.add_view(hello_world, route_name='any')
    app = config.make_wsgi_app()
    return app


if __name__ == '__main__':
    app = main()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
