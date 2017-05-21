from __future__ import absolute_import
from __future__ import unicode_literals

# important to import from .cli so that the commands get attached
from {{cookiecutter.project_namespace}}.cli import {{cookiecutter.project_class}}


def pytest_configure(config):
    {{cookiecutter.project_class}}.testing_prep()
