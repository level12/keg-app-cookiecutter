from celery.signals import setup_logging
from raven.contrib.celery import register_signal

from {{cookiecutter.project_namespace}}.app import (
    {{cookiecutter.project_class}},
    sentry
)
# By using the name "celery" `celery worker` will find the instance.
from {{cookiecutter.project_namespace}}.celery import celery_app as celery  # noqa


@setup_logging.connect
def add_handler(**kwargs):
    # This disables all Celery's logging.  We want Keg's logging configurations to apply.
    pass


# Assuming this module will only ever be called by `celery worker` and we therefore need to setup
# our application b/c it's not been done yet.
#
# You must set the {{cookiecutter.project_class.upper()}}_CONFIG_PROFILE environment variable in
# order for this to work.  See project's readme for an example.
_app = {{cookiecutter.project_class}}().init()
_app.app_context().push()

if _app.config.get('SENTRY_DSN'):
    # hook into the Celery error handler
    register_signal(sentry.client)
