import click
from keg import current_app

from ..app import {{cookiecutter.project_class}}
from ..celery import tasks


@{{cookiecutter.project_class}}.cli.group()
def celery():
    pass


@celery.command()
def ping_alive():
    alive_url = current_app.config['CELERY_ALIVE_URL']
    tasks.ping_url.apply_async((alive_url,), priority=1)


@celery.command()
@click.argument('message', default='hello')
def say(message):
    tasks.say.delay(message)
