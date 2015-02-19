#!/usr/bin/env python
#from gevent import monkey
#monkey.patch_all()
from bottle import Bottle, run
from controllers import example

root = Bottle()

if __name__ == '__main__':
    try:
        import bjoern
        server = 'bjoern'
    except ImportError:
        import gunicorn
        server ='gunicorn'
    finally:
        run(host='0.0.0.0', port=5000, server=server,
            workers=16, debug=False)
