import json
import logging

from functools import wraps

from bottle import route, static_file, request, post, get, abort

from bmgapp import view, render_template
from bmgapp.creator import Creator
from bmgapp.generator import Generator
from bmgapp.helpers import get_only_files


logger = logging.getLogger(__name__)


@route('/hello')
def hello():
    logger.info('asdfadsf')
    return "Hello World!"


@route('/')
@view('index.html')
def index(): pass


current_project = {
    'created': False
}


def with_project(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_project['created']:
            return abort(403, 'You need prepared project first')
        result = func(*args, **kwargs)
        return result
    return wrapper

""" Create project section """


@route('/creator')
@view('creator.html')
def creator():
    pass


@route('/create', method=['POST'])
def create():
    c = Creator(**request.POST)
    result = c.create()
    #todo: update dictionary with values returned from create()
    current_project['created'] = True
    current_project.update(result)
    print(current_project)
    return 'Ok'


@route('/done')
@with_project
def done():
    return render_template('done_creation.html', **current_project)


""" Generate code section """


@route('/gen')
@view('generator.html')
def generator():
    modules = get_only_files('benedict/app', ext='.py', full_path=False)
    return {'modules': modules}


@route('/check_models')
@with_project
def check_models():
    g = Generator(current_project)
    models_list = g.get_models(request.GET['module'])
    return json.dumps(models_list)


@route('/generator')
@view('generator_select.html')
def generator_select():
    pass


@post('/generate')
@with_project
def generate():
    g = Generator(current_project)
    print(request.POST.items())
    g.generate_model_data(module_name=None, model_name=request.POST['model-class'])  #todo: project-specific data from global dict
    return 'Ok'


@route('/inspect')
@with_project
def inspect():
    g = Generator(current_project)
    g.introspect()
    return 'Ok'


@route('/<folder>/<filename:path>')
def server_static(folder, filename):
    return static_file(filename, root=folder)


