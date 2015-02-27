from __future__ import absolute_import
from __future__ import unicode_literals

from {{cookiecutter.project_namespace}}.app import {{cookiecutter.project_class}}


def pytest_configure(config):
    {{cookiecutter.project_class}}.testing_prep()
