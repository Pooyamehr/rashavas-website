#!/usr/bin/env python

#__all__ = ['Base', 'IDMixin']

import bottle

from bottle.ext import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, Sequence, String, DateTime
from sqlalchemy import ForeignKey, Table, \
    Float, Boolean, event
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship, backref  # for relationships
from sqlalchemy.orm import validates, deferred
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import or_, and_
from sqlalchemy import desc, asc
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import scoped_session, sessionmaker
from uuid import uuid4
import base64
import datetime
import json as json

now = datetime.datetime.utcnow

class SP(sqlalchemy.Plugin):
        
        def __init__(self, engine, metadata=None,
                 keyword='db', commit=True, create=False, use_kwargs=False, create_session=None):
            sqlalchemy.Plugin.__init__(self, engine, metadata=None,
                 keyword='db', commit=True, create=False, use_kwargs=False, create_session=None)

        def wrapper(*args, **kwargs):
            kwargs[keyword] = session = scoped_session(self.create_session(bind=self.engine))
            try:
                rv = callback(*args, **kwargs)
                if commit:
                    session.commit()
            except (SQLAlchemyError, bottle.HTTPError):
                session.rollback()
                raise
            except bottle.HTTPResponse:
                if commit:
                    session.commit()
                raise
            finally:
                if isinstance(self.create_session, ScopedSession):
                    self.create_session.remove()
                else:
                    session.close()
            return rv




engine = create_engine('sqlite:///databases/db.sqlite', echo=False)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


class ORMClass(object):
    """The base of the Base class
    """
    query = Session.query_property()
Base = declarative_base(cls=ORMClass)





database_plugin = SP(
    engine,  # SQLAlchemy engine created with create_engine function.
    Base.metadata,  # SQLAlchemy metadata, required only if create=True.
    keyword='db',  # Keyword used to inject session database in a route (default 'db').
    create=True,  # If it is true, execute `metadata.create_all(engine)` when plugin is applied (default False).
    commit=True,  # If it is true, plugin commit changes after route is executed (default True).
    use_kwargs=False  # If it is true and keyword is not defined, plugin uses **kwargs argument to inject session database (default False).
)
bottle.install(database_plugin)
import bottle

from bottle_redis import RedisPlugin
bottle.install(RedisPlugin())


def getUUID():
    data = base64.encodestring(uuid4().get_bytes()).strip()[:-2]
    return data.replace('/', '-')


class IDMixin(object):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    #__table_args__ = {'mysql_engine': 'InnoDB'}
    #__mapper_args__= {'always_refresh': True}
    id = Column(Integer, primary_key=True)
    uuid = Column(String(64), default=getUUID)
    created_on = Column(DateTime, default=now)
    modified_on = Column(DateTime, default=now, onupdate=now)

    @property
    def columns(self):
        data = [c.name for c in self.__table__.columns]
        return data

    @property
    def columnitems(self):
        try:
            data = [(c, getattr(self, c)) for c in self.columns]
            return dict([i for i in data
                         if isinstance(i[1], (str, unicode, datetime.datetime, long, int, float, bool))])
        except AttributeError, e:
            print e
            return self.title

    def __repr__(self):
        return json.dumps(self.columnitems)









