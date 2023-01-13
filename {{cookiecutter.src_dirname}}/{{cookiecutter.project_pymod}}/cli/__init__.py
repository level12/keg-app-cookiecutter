import logging

from ..app import {{cookiecutter.project_class}}

# These imports are to get the cli sub-modules loaded.
from . import celery  # noqa
from . import cronitor  # noqa
from . import db  # noqa

log = logging.getLogger(__name__)


def cli_entry():
    {{cookiecutter.project_class}}.cli.main()


if __name__ == '__main__':
    cli_entry()
