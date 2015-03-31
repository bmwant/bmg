# -*- coding: utf-8 -*-
__author__ = 'Most Wanted'
import functools
import jinja2

env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))


def view(template_name):
    def decorator(view_func):
        @functools.wraps(view_func)
        def wrapper(*args, **kwargs):
            response = view_func(*args, **kwargs)
            template = env.get_template(template_name)

            if isinstance(response, dict):
                return template.render(**response)
            else:
                return template.render()
        return wrapper
    return decorator

