#!/usr/bin/env python

from bottle import get, post, delete, put, run, static_file
from bottle import mako_template as template
from bottle import mako_view as view
from bottle import HTTPError
from models.db import *


@get('/app')
@view('index')
def index():
    return dict(name="my project name")


@get('/db/:name')
def show(name, db, rdb):
    '''rdb is redis db.  db is a sqlite db'''
    entity = db.query(Entity).filter_by(name=name).first()
    if entity:
        return {'id': entity.id, 'name': entity.name}
    return HTTPError(404, 'Entity not found.')

@put('/db/:name')
def put_name(name, db, rdb):
    entity = Entity(name)
    db.add(entity)



@get('/<filename:path>')
def send_static(filename):
    return static_file(filename, root='views')

