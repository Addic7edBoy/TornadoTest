import asyncio

import tornado.ioloop
import tornado.web
from tornado.web import Application
from tornado.web import RequestHandler

from sqlalchemy.ext.asyncio import create_async_engine

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
        # arr = await Array.create(in_arr = '[2,1,3]', out_arr = '[1,2,3]')
        # self.write(arr)
        self.write('test')

    # def post(self):
    #     self.write("THIS IS A POST REQUEST")

class GetArraysHandler(RequestHandler):
    SUPPORTED_METHODS = ["GET"]

    def get(self, id):
        self.write(f"THIS IS A GET REQUEST WITH ID: {id}")


async def async_main():
    engine = create_async_engine("postgresql+asyncpg://postgres:postgres@localhost/postgres", echo=True, future=True)

    async with engine.begin() as conn:
        await conn.run_sync(meta.drop_all)
        await conn.run_sync(meta.create_all)

    app = tornado.web.Application([
        (r"/", HelloWorld),
        (r"/arrays", PostArraysHandler),
        (r"/arrays/([0-9]+)", GetArraysHandler)
    ])
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    asyncio.run(async_main())
