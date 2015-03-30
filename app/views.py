from bottle import route, static_file
from bottle import jinja2_view as view



@route('/hello')
def hello():
    return "Hello World!"


@route('/')
@view('index.html')
def index():
    pass


@route('/dbconfig')
@view('db.html')
def index():
    pass


@route('/<folder>/<filename:path>')
def server_static(folder, filename):
    return static_file(filename, root=folder)


