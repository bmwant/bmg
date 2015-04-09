# -*- coding: utf-8 -*-
__author__ = 'Most Wanted'
import os
import logging
import shutil

import yaml

from random import randint
from jinja2 import Template

from .helpers import get_list_of_files, get_only_files, fj

logger = logging.getLogger(__name__)


class Creator(object):

    NEED_COMPILE = ('__init__.py', 'config.py', 'models.py', 'helpers.py', )
    EXCLUDE = ('forms_header.py', 'views_header.py',)
    CONFIG_FILE = '.bmgprojects'

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

        self.run_port = randint(21721, 65535)  # port from BMG-default port to max possible
        self.secret_key = os.urandom(16).encode('hex')

    def create(self):
        dir_name = self.project_name.lower()
        if os.path.exists(dir_name):
            logger.info('Removing previous folder [%s]' % self.project_name)
            shutil.rmtree(dir_name, ignore_errors=True)
        logger.info('Creating project structure for [%s]' % self.project_name)

        #templates
        logger.info('Copying template files of %s' % self.css_framework)
        shutil.copytree(fj('boilerplate/templates', self.css_framework),
                        fj(dir_name, 'templates'))

        #css
        logger.info('Copying css files of %s' % self.css_framework)
        shutil.copytree(fj('boilerplate/static/css', self.css_framework),
                        fj(dir_name, 'static/css'))

        #js
        logger.info('Copying js files of %s' % self.css_framework)
        shutil.copytree(fj('boilerplate/static/js', self.css_framework),
                        fj(dir_name, 'static/js'))

        #app folder
        logger.info('Copying main application files')
        os.makedirs(fj(self.project_dir, 'app'))
        self.copy_files('boilerplate/app', fj(self.project_dir, 'app'),
                        exclude=self.EXCLUDE)

        #and other files
        self.copy_files('boilerplate', self.project_dir)
        self.copy_files('boilerplate/static', fj(self.project_dir, 'static'))  # favicon

        self.fill_project_data()
        project_result = self.__dict__
        self.save_project_info()
        return project_result

    def save_project_info(self):
        project_result = self.__dict__
        projects = {}
        if os.path.exists('.bmgprojects'):
            with open('.bmgprojects') as fin:
                projects.update(yaml.load(fin))
        projects[self.project_name] = project_result

        with open('.bmgprojects', 'a') as fout:
            fout.write(yaml.dump(projects))


    def copy_files(self, directory, where, exclude=None):
        for file_name in get_only_files(directory):
            if exclude is not None and os.path.basename(file_name) in exclude:
                continue
            shutil.copy(file_name, where)

    def fill_project_data(self):
        dir_name = self.project_name.lower()
        for module_file in get_list_of_files(fj(dir_name, 'app'), ext='.py'):
            file_name = os.path.basename(module_file)
            if file_name in self.NEED_COMPILE:
                self.compile_module(module_file)

    def compile_module(self, module_file):
        logger.info('Filling %s with project data' % module_file)

        with open(module_file, 'r') as fin:
            template = fin.read()

        with open(module_file, 'w') as fout:
            jinja_template = Template(template)
            result = jinja_template.render(**self.__dict__)
            fout.write(result)

