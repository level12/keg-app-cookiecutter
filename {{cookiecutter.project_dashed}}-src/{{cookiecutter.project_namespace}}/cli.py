from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

import click

from {{cookiecutter.project_namespace}}.app import {{cookiecutter.project_class}}


def cli_entry():
    {{cookiecutter.project_class}}.cli_run()


@{{cookiecutter.project_class}}.command('hello', help='say hello')
@click.option('--name', default='World', help='The person to greet.')
def hello_world(name):
    print('Hello {} from {{cookiecutter.project_name}}!'.format(name))

if __name__ == '__main__':
    cli_entry()
