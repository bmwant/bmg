from bottle import Bottle
from jinja2 import Environment, FileSystemLoader
from peewee import MySQLDatabase, PostgresqlDatabase, SqliteDatabase

from config import Config as config

{% if with_db %}
db = MySQLDatabase(config.DB_NAME,
                   host=config.DB_HOST, port=config.DB_PORT,
                   user=config.DB_USER, password=config.DB_PASS)
db.get_conn().ping(True)
{% endif %}

app = Bottle()
app.project_name = '{{ project_name }}'
#Install plugins here

env = Environment(loader=FileSystemLoader('templates'))
#Set additional template globals here
env.globals['app'] = app

#Set additional template filters here
#env.filters['filter_name'] = filter_func

#If you want to add views from another module - import them in views module
from app.views import *




