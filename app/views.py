from bottle import route, static_file, request

from app import view
from app.creator import Creator

@route('/hello')
def hello():
    return "Hello World!"


@route('/')
@view('index.html')
def index():
    pass


@route('/create', method=['POST'])
def index():
    c = Creator(**request.POST)
    c.create()
    return 'Ok'


@route('/done')
@view('done.html')
def done():
    pass


@route('/<folder>/<filename:path>')
def server_static(folder, filename):
    return static_file(filename, root=folder)


