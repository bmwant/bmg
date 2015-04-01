# -*- coding: utf-8 -*-
{% if with_db %}
from peewee import *
from app import db


class UnknownField(object):
    pass


class BaseModel(Model):
    class Meta:
        database = db
{% endif %}