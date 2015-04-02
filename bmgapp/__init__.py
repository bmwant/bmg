# -*- coding: utf-8 -*-
__author__ = 'Most Wanted'
import logging
import functools
import jinja2

env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

#Initialize logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s')
formatter.datefmt = '%H:%M:%S %d/%m/%y'
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)


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


def render_template(tpl_name, *args, **kwagrs):
    """
    Render template helper function
    """
    template = env.get_template(tpl_name)
    return template.render(*args, **kwagrs)

