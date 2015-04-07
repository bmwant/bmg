# -*- coding: utf-8 -*-
from app import env

{% if with_db %}
from app import app, db

@app.hook('before_request')
def _connect_db():
    db.connect()


@app.hook('after_request')
def _close_db():
    if not db.is_closed():
        db.close()
{% endif %}

def render_template(tpl_name, *args, **kwagrs):
    """
    Render template helper function
    """
    template = env.get_template(tpl_name)
    return template.render(*args, **kwagrs)