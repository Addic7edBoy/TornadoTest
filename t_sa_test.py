# __init__.py
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application
from tornado.web import RequestHandler
from tornado_sqlalchemy import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, ARRAY
from sqlalchemy import func
import os
import json
from tornado_sqlalchemy import make_session_factory, SessionMixin

Base = declarative_base


class Array(Base):
    __tablename__ = "arrays"
    id = Column(Integer, primary_key=True, autoincrement=True)
    in_arr = Column(ARRAY)
    out_arr = Column(ARRAY)
    create_date = Column(DateTime, server_default=func.now())
    __mapper_args__ = {"eager_defaults": True}


define('port', default=8888, help='port to listen on')
factory = make_session_factory(os.environ.get('DATABASE_URL', ''))


class BaseView(RequestHandler, SessionMixin):
    """Base view for this application."""

    def set_default_headers(self):
        """Set the default response header to be JSON."""
        self.set_header("Content-Type", 'application/json; charset="utf-8"')

    def send_response(self, data, status=200):
        """Construct and send a JSON response with appropriate status code."""
        self.set_status(status)
        self.write(json.dumps(data))


class HelloWorld(BaseView):
    """Print 'Hello, world!' as the response body."""

    def get(self):
        """Handle a GET request for saying Hello World!."""
        self.write("Hello, world!")


class InfoView(BaseView):
    """Only allow GET requests."""
    SUPPORTED_METHODS = ["GET"]

    def set_default_headers(self):
        """Set the default response header to be JSON."""
        self.set_header("Content-Type", 'application/json; charset="utf-8"')

    def get(self):
        """List of routes for this API."""
        routes = {
            'info': 'GET /api/v1',
            'register': 'POST /api/v1/accounts',
            'single profile detail': 'GET /api/v1/accounts/<username>',
            'edit profile': 'PUT /api/v1/accounts/<username>',
            'delete profile': 'DELETE /api/v1/accounts/<username>',
            'login': 'POST /api/v1/accounts/login',
            'logout': 'GET /api/v1/accounts/logout',
            "user's tasks": 'GET /api/v1/accounts/<username>/tasks',
            "create task": 'POST /api/v1/accounts/<username>/tasks',
            "task detail": 'GET /api/v1/accounts/<username>/tasks/<id>',
            "task update": 'PUT /api/v1/accounts/<username>/tasks/<id>',
            "delete task": 'DELETE /api/v1/accounts/<username>/tasks/<id>'
        }
        self.write(json.dumps(routes))

def main():
    """Construct and serve the tornado application."""
    app = Application([
        ('/', InfoView)
    ], session_factory=factory)
    http_server = HTTPServer(app)
    http_server.listen(options.port)
    print('Listening on http://localhost:%i' % options.port)
    IOLoop.current().start()
