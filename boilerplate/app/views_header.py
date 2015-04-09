import json
from bottle import request, redirect
from models import *
from gen_forms import *
from helpers import render_template
from app import app, env


class PeeweeModelEncoder(json.JSONEncoder):
    def default(self, o):
        return o._data