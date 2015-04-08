import os
import json
import logging

import yaml

from functools import wraps

from bottle import route, static_file, request, post, get, abort, redirect, HTTPResponse

from bmgapp import view, render_template
from bmgapp.creator import Creator
from bmgapp.generator import Generator
from bmgapp.helpers import get_only_files, fj


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
        print(current_project)
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
    current_project['created'] = True
    current_project.update(result)
    print(current_project)
    return 'Ok'


@route('/done')
@with_project
def done():
    return render_template('done_creation.html', **current_project)


""" Generate code section """


def load_project(name):
    #todo: load project, yaml
    current_project['created'] = True
    stream = file('.bmgprojects')
    projects = yaml.load(stream)
    current_project.update(projects[name])
    print('Current project', current_project)


def get_projects():
    if not os.path.exists('.bmgprojects'):
        return {}
    stream = file('.bmgprojects')
    projects = yaml.load(stream)
    return projects


@route('/gen_models')
@view('generator_models.html')
@with_project
def generator_models():
    app_dir = fj(current_project['project_dir'], 'app')
    modules = get_only_files(app_dir, ext='.py', full_path=False)
    return {'modules': modules}


@route('/gen_select', method=['GET', 'POST'])
@view('generator_select.html')
def generator_select():
    if request.method == 'GET':
        redirect('/generator')

    if not 'project' in request.POST:
        abort(400, 'You cannot do this without project selected')
    project_name = request.POST['project']
    load_project(project_name)
    return {'project': project_name}


@route('/check_models')
@with_project
def check_models():
    g = Generator(current_project)
    models_list = g.get_models(request.GET['module'])
    return json.dumps(models_list)


@route('/generator')
@view('generator.html')
def generator():
    projects = get_projects()
    with_db = []
    for pr_name, pr_data in projects.iteritems():
        if pr_data['with_db']:
            with_db.append(pr_data['project_name'])
    return {'projects': with_db}


@post('/generate')
@with_project
def generate():
    """
    Generates selected data for current project based on 'model_name'-model
    from 'module'-module
    """
    g = Generator(current_project)
    g.generate_model_data(module_name=request.POST['module'],
                          model_name=request.POST['model-class'])
    return 'Ok'


@route('/inspect')
@with_project
def inspect():
    """
    Inspect the database of current project and write all data to models.py
    file
    """
    if not current_project['with_db']:
        return HTTPResponse(status=500, body='This project does not have connection to database')
    g = Generator(current_project)
    g.introspect()
    return 'Ok'


@route('/<folder>/<filename:path>')
def server_static(folder, filename):
    return static_file(filename, root=folder)


