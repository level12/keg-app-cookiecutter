import logging

import click

from {{cookiecutter.project_namespace}}.app import {{cookiecutter.project_class}}
import {{cookiecutter.project_namespace}}.celery.tasks as celery_tasks

log = logging.getLogger(__name__)


def cli_entry():
    {{cookiecutter.project_class}}.cli.main()


@{{cookiecutter.project_class}}.cli.command('hello', short_help='Example command: say hello.')
@click.option('--name', default='World', help='The person to greet.')
def hello_world(name):
    click.echo('Hello {} from {{cookiecutter.project_name}}!'.format(name))


@{{cookiecutter.project_class}}.cli.command('log', short_help='log some messages')
def logcmd():
    log.info('info log message')
    log.warning('warning log message')
    log.error('error log message')


@{{cookiecutter.project_class}}.cli.group()
def celery():
    """ Celery related commands. """


@celery.command('ping')
def celery_ping():
    celery_tasks.ping.delay()


@celery.command('error')
def celery_error():
    celery_tasks.error.delay()


if __name__ == '__main__':
    cli_entry()
