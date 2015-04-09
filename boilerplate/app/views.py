# -*- coding: utf-8 -*-
from bottle import static_file, error, request, post
from app import app, env, config

from models import *
from helpers import *

try:
    from gen_views import *
except ImportError:
    pass


@app.get('/')
def index():
    return render_template('index.html')


@app.get('/about')
def about():
    return render_template('about.html')


@app.get('/components')
def components():
    return render_template('components.html')


if config.DEBUG:
    #serving static files
    @app.get('/<folder>/<filename:path>')
    def server_static(folder, filename):
        return static_file(filename, root=config.STATIC_FOLDER+folder)

    #favicon :)
    @app.route('/favicon.ico')
    def serve_favicon():
        return static_file('favicon.ico', root=config.STATIC_FOLDER)
