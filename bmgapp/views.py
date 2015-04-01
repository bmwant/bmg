import json

from bottle import route, static_file, request, post, get

from bmgapp import view, render_template
from bmgapp.creator import Creator
from bmgapp.generator import Generator
from bmgapp.helpers import get_only_files


@route('/hello')
def hello():
    return "Hello World!"


@route('/')
@view('index.html')
def index(): pass


current_project = {}

""" Create project section """


@route('/creator')
@view('creator.html')
def creator():
    pass


@route('/create', method=['POST'])
def create():
    c = Creator(**request.POST)
    c.create()
    current_project['run_port'] = c.run_port
    return 'Ok'


@route('/done')
def done():
    return render_template('done.html', **current_project)


""" Generate code section """


@route('/gen')
@view('generator.html')
def generator():
    modules = get_only_files('benedict/app', ext='.py', full_path=False)
    return {'modules': modules}


@route('/check_models')
def check_models():
    g = Generator()
    print(request.GET['module'])
    models_list = g.get_models(request.GET['module'])
    print(models_list)
    return json.dumps(models_list)


@route('/generator')
@view('generator_select.html')
def generator_select():
    pass


@post('/generate')
def generate():
    print(request.POST.items())
    return 'Ok'


@route('/inspect')
def inspect():
    g = Generator()
    g.introspect()
    return 'Ok'


@route('/<folder>/<filename:path>')
def server_static(folder, filename):
    return static_file(filename, root=folder)


