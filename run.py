from bottle import run
from app.views import *


if __name__ == '__main__':
    run(host='localhost', port=21721, debug=True, reloader=True)