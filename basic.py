from sqlalchemy import BigInteger, Column, String
from tornado.gen import coroutine
from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler
from tornado.options import define, options

from tornado_sqlalchemy import SessionMixin, as_future, SQLAlchemy

define('port', default=8888, help='port to listen on')

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    username = Column(String(255), unique=True)


class SynchronousRequestHandler(SessionMixin, RequestHandler):
    def get(self):
        with self.make_session() as session:
            count = session.query(User).count()

        # OR count = self.session.query(User).count()

        self.write('{} users so far!'.format(count))


class GenCoroutinesRequestHandler(SessionMixin, RequestHandler):
    @coroutine
    def get(self):
        with self.make_session() as session:
            count = yield as_future(session.query(User).count)

        self.write('{} users so far!'.format(count))


class NativeCoroutinesRequestHandler(SessionMixin, RequestHandler):
    async def get(self):
        with self.make_session() as session:
            count = await as_future(session.query(User).count)

        self.write('{} users so far!'.format(count))


if __name__ == '__main__':
    db.configure(url='sqlite://')

    app = Application(
        [
            (r'/sync', SynchronousRequestHandler),
            (r'/gen-coroutines', GenCoroutinesRequestHandler),
            (r'/native-coroutines', NativeCoroutinesRequestHandler),
        ],
        db=db,
    )

    app.listen(options.port)
    print('Listening on port 8888')

    IOLoop.current().start()
