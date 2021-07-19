from sqlalchemy import BigInteger, Column, String, DateTime, Integer
from sqlalchemy import func
from tornado.gen import coroutine
from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler
from tornado.options import define, options
import json
from datetime import datetime
import ast
import os

from tornado_sqlalchemy import SessionMixin, as_future, SQLAlchemy


define('port', default=8888, help='port to listen on')

db = SQLAlchemy()


def date_2_str(o):
    if isinstance(o, datetime):
        return o.__str__()

class Array(db.Model):
    __tablename__ = "arrays"

    id = Column(Integer, primary_key=True, autoincrement=True)
    in_arr = Column(String)
    out_arr = Column(String)
    create_date = Column(DateTime, server_default=func.now())

    __mapper_args__ = {"eager_defaults": True}


class BaseView(RequestHandler, SessionMixin):

    def prepare(self):
        self.form_data = {
            key: [val.decode('utf8') for val in val_list]
            for key, val_list in self.request.arguments.items()
        }

    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json; charset="utf-8"')

    def send_response(self, data, status=200):
        self.set_status(status)
        self.write(json.dumps(data, default=date_2_str))

    async def get_array(self, id):
        with self.make_session() as session:
            try:
                arr = await as_future(session.query(Array).filter(Array.id == id).first)
                # name = user.username
                if arr:
                    # create = str(datetime.strptime(arr.create_date, '%d/%m/%Y %H:%M:%S'))
                    self.send_response({'id': arr.id, 'in_arr': json.loads(
                        arr.in_arr), 'out_arr': json.loads(arr.out_arr), 'create_date': arr.create_date})
                else:
                    self.send_response(data={'result': 'ERROR'}, status=404)
            except:
                self.send_response(data={'result': 'ERROR'}, status=500)


class FetchArrayHandler(BaseView):
    async def get(self, id):
        await self.get_array(id)

class AddArrayHandler(BaseView):
    async def post(self):
        with self.make_session() as session:
            # create = datetime.now()

            in_arr = json.loads(self.form_data['in_arr'][0])
            sorted_arr = sorted(in_arr)
            new_arr = Array(
                in_arr = str(in_arr),
                out_arr = str(sorted_arr)
                # create_date=datetime.strptime(create, '%d/%m/%Y %H:%M:%S')
            )
            session.add(new_arr)
            session.commit()
            self.send_response({'result': 'OK', 'id': new_arr.id})
    async def get(self):
        id = self.get_argument('id')
        if not id:
            self.send_response(data={'result': 'ERROR'}, status=500)
            return
        await self.get_array(id)

class InfoHandler(BaseView):
    async def get(self):
        with self.make_session() as session:
            count = await as_future(session.query(Array).count)

        self.send_response({'Arrays count': count})

if __name__ == '__main__':
    pg = {
        'user': os.environ.get('DB_USER', 'max'),
        'password': os.environ.get('DB_PASS', '8883868'),
        'host': os.environ.get('DB_HOST', 'localhost'),
        'port': os.environ.get('DB_PORT', 5432),
        'db': os.environ.get('DB_NAME', 'max')
    }
    db.configure(url=f"postgresql://{pg['user']}:{pg['password']}@{pg['host']}:{pg['port']}/{pg['db']}")

    app = Application(
        [
            (r"/", InfoHandler),
            (r"/arrays", AddArrayHandler),
            (r"/arrays/([0-9]+)", FetchArrayHandler),
        ],
        db=db,
    )

    # db.create_all()

    # session = db.sessionmaker()
    # session.add(Array(in_arr='[3,4,5,2,1]', out_arr='[1,2,3,4,5]'))
    # session.commit()
    # session.close()

    app.listen(options.port)
    print(f'Listening on port {options.port}')

    IOLoop.current().start()
