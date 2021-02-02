import logging

import flask
from keg.db import db
from keg.web import BaseView

from {{cookiecutter.project_namespace}}.celery import tasks as ctasks

log = logging.getLogger(__name__)
public_bp = flask.Blueprint('public', __name__,)


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
