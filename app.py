#!/usr/bin/env python

from bottle import get, post, delete, put, run, view, template, static_file
from bottle import HTTPError
from models.db import *


@get('/app')
@view('index')
def index():
    return dict(name="ok")


@get('/db/:name')
def show(name, db):
    entity = db.query(Entity).filter_by(name=name).first()
    if entity:
        return {'id': entity.id, 'name': entity.name}
    return HTTPError(404, 'Entity not found.')

@put('/db/:name')
def put_name(name, db):
    entity = Entity(name)
    db.add(entity)



@get('/<filename:path>')
def send_static(filename):
    return static_file(filename, root='views')


if __name__ == '__main__':
    run(host='localhost', port=8080, server='gunicorn',
        workers=4, debug=True)
