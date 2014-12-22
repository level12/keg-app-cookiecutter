from __future__ import absolute_import
from __future__ import unicode_literals

from {{cookiecutter.project_namespace}}.app import {{cookiecutter.project_class}}


def pytest_configure(config):
    app = {{cookiecutter.project_class}}.create_app(config_profile='Test')
    app.test_request_context().push()
