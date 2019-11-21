import logging

from {{cookiecutter.project_namespace}}.app import {{cookiecutter.project_class}}

# These imports are to get cli sub-modules loaded.
from ..cli import celery  # noqa
from ..cli import db  # noqa

log = logging.getLogger(__name__)


def cli_entry():
    {{cookiecutter.project_class}}.cli.main()


@{{cookiecutter.project_class}}.cli.command('log', short_help='log some messages')
def logcmd():
    log.info('info log message')
    log.warning('warning log message')
    log.error('error log message')


if __name__ == '__main__':
    cli_entry()
