import logging

import flask
from keg.db import db
from keg.web import BaseView, rule

from {{cookiecutter.project_namespace}}.celery import tasks as ctasks

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


class HealthCheck(BaseView):
    """ An endpoint our monitoring service can watch that, unlike Keg's /ping, will also
        test connectivity to the DB before returning an "ok" message.
    """
    blueprint = public_bp

    def get(self):
        # We are happy if this doesn't throw an exception.  Nothing to test b/c we aren't sure
        # there will be a user record.
        db.engine.execute('select id from users limit 1').fetchall()

        # Log aggregator (e.g. Loggly) can alert on this as a "heartbeat" for the app assuming
        # something like Cronitor is hitting this URL repeatedly to monitor uptime.
        log.info('ping-db ok')

        alive_url = flask.current_app.config['CELERY_ALIVE_URL']

        ctasks.ping_url.apply_async((alive_url,), priority=10)

        return '{} ok'.format(flask.current_app.name)


class AlertsDemo(BaseView):
    blueprint = public_bp
    template_name = 'base-page.html'

    def get(self):
        flask.flash('Success message', 'success')
        flask.flash('Info message', 'info')
        flask.flash('Warning message', 'warning')
        flask.flash('Error message', 'error')
        flask.flash('Danger message', 'danger')
