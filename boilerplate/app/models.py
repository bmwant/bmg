# -*- coding: utf-8 -*-
{% if with_db %}
from peewee import *
from bottle import abort
from app import db


class UnknownField(object):
    pass


class BaseModel(Model):
    @classmethod
    def get_or_404(cls, *query, **kwargs):
        try:
            inst = cls.get(*query, **kwargs)
            return inst
        except DoesNotExist:
            abort(404)

    def __str__(self):
        if hasattr(self, 'id'):
            return '%s # %s' % (type(self).__name__, str(self.id))
        return type(self).__name__

    class Meta:
        database = db
{% endif %}