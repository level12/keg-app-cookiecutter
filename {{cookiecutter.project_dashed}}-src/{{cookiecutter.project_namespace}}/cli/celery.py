from keg import current_app

from {{cookiecutter.project_namespace}}.app import {{cookiecutter.project_class}}
from {{cookiecutter.project_namespace}}.celery import tasks


@{{cookiecutter.project_class}}.cli.group()
def celery():
    pass


@celery.command()
def ping():
    alive_url = current_app.config['CELERY_ALIVE_URL']
    tasks.ping_url.apply_async((alive_url,), priority=1)
