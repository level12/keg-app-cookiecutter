import _pytest.config.findpaths
import keg
import pytest
from keg.db import db
from keg.testing import ContextManager

import {{cookiecutter.project_pymod}}
import {{cookiecutter.project_pymod}}.celery.testing as ct
import {{cookiecutter.project_pymod}}.libs.db as libs_db

# important to import from .cli so that the commands get attached
from {{cookiecutter.project_pymod}}.cli import {{cookiecutter.project_class}}

# You can uncomment this if you end up with asserts in libraries outside tests.
# pytest.register_assert_rewrite('{{cookiecutter.project_pymod}}.libs.testing')

pytest_plugins = ('celery.contrib.pytest',)


def pytest_configure(config):
    add_ci_filterwarnings(config)

    {{cookiecutter.project_class}}.testing_prep(
        TESTING_DB_RESTORE=config.getoption('db_restore'),
        SQLALCHEMY_ECHO=config.getoption('db_echo'),
    )


@pytest.fixture(scope='class', autouse=True)
def auto_app_context():
    with ContextManager.get_for({{cookiecutter.project_class}}).app.app_context():
        yield


@pytest.fixture(scope='module')
def module_app_context():
    with ContextManager.get_for({{cookiecutter.project_class}}).app.app_context():
        yield


@pytest.fixture()
def app_context():
    with ContextManager.get_for({{cookiecutter.project_class}}).app.app_context():
        yield


@pytest.fixture(scope='session')
def celery_config():
    """Need to setup custom task annotations so the task tracker works correctly."""
    with ContextManager.get_for({{cookiecutter.project_class}}).app.app_context():
        config = keg.current_app.config['CELERY'].copy()
    annotations = {'*': {
        'after_return': ct.after_return_handler,
        'before_start': ct.before_start_handler,
        'on_retry': ct.on_retry_handler,
    }}
    config['task_annotations'] = annotations
    return config


@pytest.fixture(scope='session')
def celery_worker_parameters():
    """Need a custom Worker class that initializes the Keg app in the worker's thread."""
    return {'WorkController': ct.TestWorkController}


@pytest.fixture
def reflect_db():
    with libs_db.reflect_db(db.engine) as (classes, session):
        yield classes, session


def pytest_addoption(parser):
    parser.addoption('--db-restore', action='store_true', default=False, dest='db_restore')
    parser.addoption('--db-echo', action='store_true', default=False, dest='db_echo')


def add_ci_filterwarnings(pytest_config):
    """
    When running tests, devs should have the same pytest warning configuration as is setup
    in CI.  Pytest does not permit multiple pytest.ini config files.  Furthermore, if we set
    a pytest.ini at the project level then a dev's personal pytest.ini options get ignored.
    This function grabs the filterwarnings from .ci/pytest.ini and adds them to the pytest
    config (if they aren't there already).
    This is defined here and not in .libs.testing because we use register_assert_rewrite()
    on .libs.testing and importing from that module at the top level of this file will
    cause the assert rewrite to fail.
    """
    ci_ini_fpath = {{cookiecutter.project_pymod}}.src_dpath / '.ci' / 'pytest.ini'

    ci_ini_cfg = _pytest.config.findpaths.load_config_dict_from_file(ci_ini_fpath)
    existing_filterwarnings = pytest_config.inicfg.get('filterwarnings', '')
    # In CI, pytest will already be using .ci/pytest.ini
    if existing_filterwarnings != ci_ini_cfg['filterwarnings']:
        print(f'Applying filterwarnings from: {ci_ini_fpath}')
        pytest_config.inicfg['filterwarnings'] = (
            existing_filterwarnings + ci_ini_cfg['filterwarnings']
        )
        del pytest_config._inicache['filterwarnings']
