from bottle import run, TEMPLATE_PATH
from app.views import *

TEMPLATE_PATH[:] = ['templates']


if __name__ == '__main__':
    run(host='localhost', port=21721, debug=True, reloader=True)