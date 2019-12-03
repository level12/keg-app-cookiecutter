import logging

from {{cookiecutter.project_namespace}}.app import {{cookiecutter.project_class}}

# This import is to get a cli sub-module loaded.
from ..cli import db  # noqa

log = logging.getLogger(__name__)


def cli_entry():
    {{cookiecutter.project_class}}.cli.main()


if __name__ == '__main__':
    cli_entry()
