from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import ARRAY

from db import Base, async_db_session


class ModelAdmin:
    @classmethod
    async def create(cls, **kwargs):
        async_db_session.add(cls(**kwargs))
        await async_db_session.commit()

    @classmethod
    async def update(cls, id, **kwargs):
        query = (
            sqlalchemy_update(cls)
            .where(cls.id == id)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )

        await async_db_session.execute(query)
        await async_db_session.commit()

    @classmethod
    async def get(cls, id):
        query = select(cls).where(cls.id == id)
        results = await async_db_session.execute(query)
        (result,) = results.one()
        return result


class Array(Base, ModelAdmin):
    __tablename__ = "arrays"

    id = Column(Integer, primary_key=True, autoincrement=True)
    in_arr = Column(ARRAY)
    out_arr = Column(ARRAY)
    create_date = Column(DateTime, server_default=func.now())
    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}>("
            f"id={self.id}, "
            f"in_arr={self.in_arr}, "
            f"out_arr={self.out_arr}, "
            f"create_date={self.create_date}, "
            f")>"
        )

class User(Base, ModelAdmin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String)
    posts = relationship("Post")

    # required in order to acess columns with server defaults
    # or SQL expression defaults, subsequent to a flush, without
    # triggering an expired load
    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id}, "
            f"full_name={self.full_name}, "
            f"posts={self.posts}, "
            f")>"
        )


class Post(Base, ModelAdmin):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(ForeignKey("users.id"))
    data = Column(String)

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}(" f"id={self.id}, " f"data={self.data}" f")>"
        )

    @classmethod
    async def filter_by_user_id(cls, user_id):
        query = select(cls).where(cls.user_id == user_id)
        posts = await async_db_session.execute(query)
        return posts.scalars().all()
