from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application
from tornado.web import RequestHandler
import json
from tornado_sqlalchemy import SQLAlchemy, SessionMixin

import asyncio

from db import async_db_session
from models import Post, User, Array

database_url = "postgresql://user:password@localhost:port/database"


define('port', default=8888, help='port to listen on')


class BaseView(RequestHandler):
    """Base view for this application."""

    def set_default_headers(self):
        """Set the default response header to be JSON."""
        self.set_header("Content-Type", 'application/json; charset="utf-8"')

    def send_response(self, data, status=200):
        """Construct and send a JSON response with appropriate status code."""
        self.set_status(status)
        self.write(json.dumps(data))

class HelloWorld(RequestHandler):
    """Print 'Hello, world!' as the response body."""

    def get(self):
        """Handle a GET request for saying Hello World!."""
        self.write("Hello, world!")

class PostArraysHandler(RequestHandler):
    SUPPORTED_METHODS = ["POST"]

    def post(self):
        self.write("THIS IS A POST REQUEST")

class GetArraysHandler(RequestHandler):
    SUPPORTED_METHODS = ["GET"]

    def get(self, id):
        self.write(f"THIS IS A GET REQUEST WITH ID: {id}")

async def main():
    """Construct and serve the tornado application."""
    await async_db_session.init()
    await async_db_session.create_all()
    app = Application([
        (r"/", HelloWorld),
        (r"/arrays", PostArraysHandler),
        (r"/arrays/([0-9]+)", GetArraysHandler)
    ], db = SQLAlchemy(database_url))

    http_server = HTTPServer(app)
    http_server.listen(options.port)
    print('Listening on http://localhost:%i' % options.port)
    IOLoop.current().start()


if __name__ == '__main__':
    main()
