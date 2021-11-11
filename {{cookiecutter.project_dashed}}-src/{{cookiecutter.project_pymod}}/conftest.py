import keg
from keg.db import db
import pytest

import {{cookiecutter.project_pymod}}.celery.testing as ct
# important to import from .cli so that the commands get attached
from {{cookiecutter.project_pymod}}.cli import {{cookiecutter.project_class}}
import {{cookiecutter.project_pymod}}.libs.db as libs_db

# You can uncomment this if you end up with asserts in libraries outside tests.
# pytest.register_assert_rewrite('{{cookiecutter.project_pymod}}.libs.testing')

pytest_plugins = ('celery.contrib.pytest',)


def pytest_configure(config):
    {{cookiecutter.project_class}}.testing_prep(
        TESTING_DB_RESTORE=config.getoption('db_restore'),
        SQLALCHEMY_ECHO=config.getoption('db_echo'),
    )


def pytest_runtest_setup():
    # Avoid a messed up transaction interfering with other tests.
    db.session.rollback()


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


@pytest.fixture
def reflect_db():
    with libs_db.reflect_db(db.engine) as (classes, session):
        yield classes, session


def pytest_addoption(parser):
    parser.addoption('--db-restore', action='store_true', default=False, dest='db_restore')
    parser.addoption('--db-echo', action='store_true', default=False, dest='db_echo')
