from bottle import route, run, jinja2_view, static_file

@route('/hello')
def hello():
    return "Hello World!"

@route('/')
@jinja2_view('index.html', template_lookup=['../templates'])
def index():
    return {}

@route('/dbconfig')
@jinja2_view('db.html', template_lookup=['../templates'])
def index():
    return {}

@route('/<folder>/<filename:path>')
def server_static(folder, filename):
    return static_file(filename, root='../'+folder)


run(host='localhost', port=21721, debug=True)