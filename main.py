import tornado.ioloop
import tornado.web
from tornado.web import Application
from tornado.web import RequestHandler

import asyncio

from db import async_db_session
from models import Array


async def init_app():
    await async_db_session.init()
    await async_db_session.create_all()


async def create_array(arr):
    arr = await Array.create(arr)
    return arr.id


async def get_array(id):
    arr = await Array.get(id)
    return arr


# asyncio.run(async_main())

class HelloWorld(RequestHandler):
    """Print 'Hello, world!' as the response body."""

    def get(self):
        """Handle a GET request for saying Hello World!."""
        self.write("Hello, world!")

class PostArraysHandler(RequestHandler):
    # SUPPORTED_METHODS = ["POST"]
    SUPPORTED_METHODS = ["GET"]

    async def get(self):
        arr = await Array.create(in_arr = '[2,1,3]', out_arr = '[1,2,3]')
        self.write(arr)

    # def post(self):
    #     self.write("THIS IS A POST REQUEST")

class GetArraysHandler(RequestHandler):
    SUPPORTED_METHODS = ["GET"]

    def get(self, id):
        self.write(f"THIS IS A GET REQUEST WITH ID: {id}")


def make_app():
    await async_db_session.init()
    await async_db_session.create_all()
    app = tornado.web.Application([
        (r"/", HelloWorld),
        (r"/arrays", PostArraysHandler),
        (r"/arrays/([0-9]+)", GetArraysHandler)
    ])
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    make_app()
