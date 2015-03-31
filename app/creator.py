# -*- coding: utf-8 -*-
__author__ = 'Most Wanted'
import os
import logging
import shutil

logger = logging.getLogger(__name__)


class Creator(object):

    def __init__(self, name, username, dbbackend, port, host, password, dbname, cssframework='', *args, **kwargs):
        self.project_name = name
        self.db_user = username
        self.db_password = password
        self.db_name = dbname
        self.db_backend = dbbackend
        self.db_host = host
        self.db_port = port
        self.css_framework = cssframework

    def create(self):
        dir_name = self.project_name.lower()
        if os.path.exists(dir_name):
            logger.info('Removing previous folder [%s]' % self.project_name)
            shutil.rmtree(dir_name, ignore_errors=True)
        logger.info('Creating project structure for [%s]' % self.project_name)
        shutil.copytree('boilerplate', dir_name)


    def fill_project_data(self):
        pass