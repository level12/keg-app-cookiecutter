from __future__ import absolute_import
from __future__ import print_function

import logging

import click

from {{cookiecutter.project_namespace}}.app import {{cookiecutter.project_class}}

log = logging.getLogger(__name__)


def cli_entry():
    {{cookiecutter.project_class}}.cli_run()


@{{cookiecutter.project_class}}.command('hello', short_help='Example command: say hello.')
@click.option('--name', default='World', help='The person to greet.')
def hello_world(name):
    click.echo('Hello {} from {{cookiecutter.project_name}}!'.format(name))


@{{cookiecutter.project_class}}.command('log', short_help='log some messages')
def logcmd():
    log.info('info log message')
    log.warning('warning log message')
    log.error('error log message')


if __name__ == '__main__':
    cli_entry()
