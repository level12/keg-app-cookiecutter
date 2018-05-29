import keg
import pytest

import {{cookiecutter.project_namespace}}.celery.testing as ct
# important to import from .cli so that the commands get attached
from {{cookiecutter.project_namespace}}.cli import {{cookiecutter.project_class}}

# You can uncomment this if you end up with asserts in libraries outside tests.
# pytest.register_assert_rewrite('{{cookiecutter.project_namespace}}.libs.testing')


def pytest_configure(config):
    {{cookiecutter.project_class}}.testing_prep()


@pytest.fixture(scope='session')
def celery_config():
    """ Need to setup custom task annotations so the task tracker works correctly. """
    config = keg.current_app.config['CELERY'].copy()
    annotations = {'*': {'after_return': ct.after_return_handler}}
    config['task_annotations'] = annotations
    return config


@pytest.fixture(scope='session')
def celery_worker_parameters():
    """ Need a custom Worker class that initializes the Keg app in the worker's thread. """
    return {'WorkController': ct.TestWorkController}
