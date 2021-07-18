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
    in_arr = Column(String)
    out_arr = Column(String)
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
