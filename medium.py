import tornado.ioloop
from tornado.web import Application, RequestHandler
from tornado_sqlalchemy import SQLAlchemy


database_url = "postgresql://user:password@localhost:port/database"
db = SQLAlchemy(database_url)


class MainHandler(RequestHandler):
    async def get(self):
       data = await lots_of_data_func()
       self.write({"data": data})


def routes():
    return Application([
        (r"/", MainHandler),
    ], db=db)


if __name__ == "__main__":
    app = routes()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
