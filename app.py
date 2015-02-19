#!/usr/bin/env python

def getControlers():
    from bottle import Bottle
    ## Import your apps here
    #*************************************************************
    from controllers import example

    #*************************************************************
    ##
    root = Bottle()



if __name__ == '__main__':
    try:
        from gevent import monkey
        monkey.patch_all()
        server = 'gevent'
    except ImportError:
        import gunicorn
        server ='gunicorn'
    finally:
        from bottle import run
        getControlers()
        run(host='0.0.0.0', port=5000, server=server,
            debug=False)
