# -*- coding: utf-8 -*-
class Config(object):
    SECRET_KEY = 'some-secret-key'
    DB_NAME = ''
    DB_USER = ''
    DB_PASS = ''
    DEBUG = True
    RELOADER = True
    RUN_HOST = '127.0.0.1'
    RUN_PORT = 8778
    STATIC_FOLDER = 'static/'


class DevelopmentConfig(Config):
    """
    Specify all additional configuration variables here.
    Also you can create as many configurations as you want with their own
    unique parameters.
    """
    pass