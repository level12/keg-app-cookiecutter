from __future__ import absolute_import
from __future__ import unicode_literals

from {{cookiecutter.project_namespace}}.version import VERSION


def cli_entry():
    print('Hello World!')
    print('From {{cookiecutter.project_name}} version {}'.format(VERSION))
