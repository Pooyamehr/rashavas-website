from bottle import route, run, view, template, static_file

@route('/app')
@view('index')
def index():
    '''test me'''
    return dict(name="ok")



@route('/<filename:path>')
def send_static(filename):
    return static_file(filename, root='views')




run(host='localhost', port=8080, server='gunicorn',
    reload=True, workers=4, debug=True)
