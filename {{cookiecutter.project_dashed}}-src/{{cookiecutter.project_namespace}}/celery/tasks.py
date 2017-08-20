import logging

from {{cookiecutter.project_namespace}}.celery import celery_app as app

log = logging.getLogger(__name__)


@app.task
def error():
    raise ValueError('celery error task')


@app.task
def ping():
    log.info('ping-pong')
