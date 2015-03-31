# -*- coding: utf-8 -*-
from bottle import static_file, error, request, post


from models import *

#from gen_views import *
from helpers import *

from app import app, env, config


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
