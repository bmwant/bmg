# -*- coding: utf-8 -*-
__author__ = 'Most Wanted'
import os
import logging
import shutil

from random import randint
from jinja2 import Template

from .helpers import get_list_of_files, get_only_files

logger = logging.getLogger(__name__)

fj = os.path.join  # Folder join


class Creator(object):

    def __init__(self, name, username, dbbackend, port, host, password, dbname, cssframework, *args, **kwargs):
        self.project_name = name
        self.project_dir = name.lower()

        self.with_db = True
        if dbbackend == 'nodb':
            self.with_db = False
        else:
            self.db_user = username
            self.db_password = password
            self.db_name = dbname
            self.db_backend = dbbackend
            self.db_host = host
            self.db_port = port
        self.css_framework = cssframework

        self.NEED_COMPILE = ('__init__.py', 'config.py', 'models.py',)

        self.run_port = randint(21721, 65535)  # port from BMG-default port to max possible
        self.secret_key = os.urandom(16).encode('hex')

    def create(self):
        dir_name = self.project_name.lower()
        if os.path.exists(dir_name):
            logger.info('Removing previous folder [%s]' % self.project_name)
            shutil.rmtree(dir_name, ignore_errors=True)
        logger.info('Creating project structure for [%s]' % self.project_name)

        #templates
        shutil.copytree(fj('boilerplate/templates', self.css_framework),
                        fj(dir_name, 'templates'))

        #css
        shutil.copytree(fj('boilerplate/static/css', self.css_framework),
                        fj(dir_name, 'static/css'))

        #js
        shutil.copytree(fj('boilerplate/static/js', self.css_framework),
                        fj(dir_name, 'static/js'))

        #app folder
        shutil.copytree('boilerplate/app', fj(dir_name, 'app'))

        #and other files
        self.copy_files('boilerplate')

        self.fill_project_data()

    def copy_files(self, directory):
        for file_name in get_only_files(directory):
            shutil.copy(file_name, self.project_dir)

    def fill_project_data(self):
        dir_name = self.project_name.lower()
        for module_file in get_list_of_files(fj(dir_name, 'app'), ext='.py'):
            file_name = os.path.basename(module_file)
            if file_name in self.NEED_COMPILE:
                self.compile_module(module_file)

    def compile_module(self, module_file):
        print('Compiling %s' % module_file)

        with open(module_file, 'r') as fin:
            template = fin.read()

        with open(module_file, 'w') as fout:
            jinja_template = Template(template)
            result = jinja_template.render(with_db=False, run_port=self.run_port, secret_key=self.secret_key)
            fout.write(result)

