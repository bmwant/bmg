# -*- coding: utf-8 -*-
__author__ = 'Most Wanted'

from playhouse.reflection import Introspector
from peewee import print_, MySQLDatabase
import pwiz
from pwiz import print_models

from .helpers import to_file


class Generator(object):

    def __init__(self):
        pass

    def introspect(self):
        db = MySQLDatabase('bmgtest', host='127.0.0.1', port=3306, user='root', password='')
        introspector = Introspector.from_database(db)
        with to_file('boilerplate/app/models.py'):
            self.print_models(introspector)

    def print_models(self, introspector, tables=None):
        database = introspector.introspect()
        print_('')
        print_('')

        def _print_table(table, seen, accum=None):
            accum = accum or []
            foreign_keys = database.foreign_keys[table]
            for foreign_key in foreign_keys:
                dest = foreign_key.dest_table

                # In the event the destination table has already been pushed
                # for printing, then we have a reference cycle.
                if dest in accum and table not in accum:
                    print_('# Possible reference cycle: %s' % dest)

                # If this is not a self-referential foreign key, and we have
                # not already processed the destination table, do so now.
                if dest not in seen and dest not in accum:
                    seen.add(dest)
                    if dest != table:
                        _print_table(dest, seen, accum + [table])

            print_('class %s(BaseModel):' % database.model_names[table])
            columns = database.columns[table]
            primary_keys = database.primary_keys[table]
            for name, column in sorted(columns.items()):
                skip = all([
                    name == 'id',
                    len(primary_keys) == 1,
                    column.field_class in introspector.pk_classes])
                if skip:
                    continue
                if column.primary_key and len(primary_keys) > 1:
                    # If we have a CompositeKey, then we do not want to explicitly
                    # mark the columns as being primary keys.
                    column.primary_key = False

                print_('    %s' % column.get_field())

            print_('')
            print_('    class Meta:')
            print_('        db_table = \'%s\'' % table)
            if introspector.schema:
                print_('        schema = \'%s\'' % introspector.schema)
            if len(primary_keys) > 1:
                pk_field_names = sorted([
                    field.name for col, field in columns.items()
                    if col in primary_keys])
                pk_list = ', '.join("'%s'" % pk for pk in pk_field_names)
                print_('        primary_key = CompositeKey(%s)' % pk_list)
            print_('')

            seen.add(table)

        seen = set()
        for table in sorted(database.model_names.keys()):
            if table not in seen:
                if not tables or table in tables:
                    _print_table(table, seen)

    def get_models(self, models_file):
        return ['Book', 'Author', 'User', 'City']