import click

from ..app import {{cookiecutter.project_class}}
from ..celery import tasks


@{{cookiecutter.project_class}}.cli.group()
def celery():
    pass


@celery.command()
def ping_alive():
    tasks.cronitor_ping('CRONITOR_CELERY_ALIVE', 'complete')


@celery.command()
@click.argument('message', default='hello')
def say(message):
    tasks.say.delay(message)
