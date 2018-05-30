
from {{cookiecutter.project_namespace}}.app import {{cookiecutter.project_class}}
import {{cookiecutter.project_namespace}}.celery.tasks as celery_tasks


@{{cookiecutter.project_class}}.cli.group()
def celery():
    """ Celery related commands. """


@celery.command('ping')
def celery_ping():
    celery_tasks.ping.delay()


@celery.command('error')
def celery_error():
    celery_tasks.error.delay()
