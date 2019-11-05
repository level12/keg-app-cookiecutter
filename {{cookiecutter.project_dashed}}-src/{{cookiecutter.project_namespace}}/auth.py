import logging

import flask
from keg.db import db
from keg.web import BaseView
from keg_auth import make_blueprint
from keg_auth.forms import user_form as user_form_base
from keg_auth.views import User as UserBase

from {{cookiecutter.project_namespace}}.celery import tasks as ctasks
from {{cookiecutter.project_namespace}}.extensions import auth_manager

log = logging.getLogger(__name__)


def user_form(config, allow_superuser, endpoint, fields=['name', 'is_enabled']):
    return user_form_base(config, allow_superuser, endpoint, fields=fields)


class User(UserBase):
    # need to make this a static method so it isn't bound on the view instance
    form_cls = staticmethod(user_form)


# This blueprint is for keg-auth's views (Login, user management, etc.)
auth_bp = make_blueprint(__name__, auth_manager, user_crud_cls=User)
private_bp = flask.Blueprint('private', __name__,)
public_bp = flask.Blueprint('public', __name__,)
blueprints = (auth_bp, public_bp, private_bp,)


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
