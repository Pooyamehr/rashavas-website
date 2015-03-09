#!/usr/bin/env python


def getControlers():
    ## Import your apps here
    #*************************************************************

    from controllers import example

    #*************************************************************











getControlers()
from bottle import Bottle, run
root = Bottle()

try:
    import gunicorn
    server ='gunicorn'
except ImportError:
    server = 'auto'
finally:
    import multiprocessing
    cpc = multiprocessing.cpu_count()
    run(host='0.0.0.0', port=5000, server=server,
        workers=cpc*2+1, debug=False)
