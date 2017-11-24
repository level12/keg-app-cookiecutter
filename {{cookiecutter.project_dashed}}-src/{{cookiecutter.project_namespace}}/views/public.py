import logging

import flask
from keg.db import db
from keg.web import BaseView, rule

public_bp = flask.Blueprint('public', __name__,)
log = logging.getLogger(__name__)


@public_bp.route('/')
def home():
    return 'Hello World from {{cookiecutter.project_name}}!'


class Hello(BaseView):
    blueprint = public_bp
    rule('<name>')

    def get(self, name='World'):
        self.assign('name', name)


class PingDB(BaseView):
    """ An endpoint our monitoring service can watch that, unlike Keg's /ping, will also
        test connectivity to the DB before returning an "ok" message.
    """
    blueprint = public_bp

    def get(self):
        # We are happy if this doesn't throw an exception.  Nothing to test b/c we aren't sure
        # there will be a user record.
        db.engine.execute('select id from users limit 1').fetchall()
        return '{} ok'.format(flask.current_app.name)
