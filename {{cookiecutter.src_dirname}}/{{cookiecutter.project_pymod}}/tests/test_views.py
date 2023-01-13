import flask
import flask_webtest as webtest
import pytest
from keg_auth.testing import AuthTestApp
from unittest.mock import call

from ..libs.testing import mock_patch
from ..model import entities as ents


# Scope needs to be class level b/c ViewTestBase clears out users in setup_class()
@pytest.fixture(scope='class')
def auth_client(perms=None):
    return AuthTestApp(flask.current_app, user=ents.User.testing_create(permissions=perms))


class TestPublic:
    @classmethod
    def setup_class(cls):
        # anonymous user
        cls.client = webtest.TestApp(flask.current_app)

    @mock_patch('{{cookiecutter.project_pymod}}.views.public.ping_cronitor')
    def test_health_check(self, m_ping_cronitor):
        # Use this for cronitor.
        resp = self.client.get('/health-check')
        assert resp.text == '{{cookiecutter.project_pymod}} ok'
        assert m_ping_cronitor.apply_async.mock_calls == [call(('celery-alive',), priority=1)]


def test_exception(self):
    # This tests the app exception route, not Kegs.
    # Refs: https://github.com/level12/keg-app-cookiecutter/issues/130
    with pytest.raises(Exception) as excinfo:
        self.client.get('/exception')
    assert str(excinfo.value) == 'Deliberate exception for testing purposes'


def test_home(self, auth_client):
    resp = self.client.get('/')
    assert resp.pyquery('main p').text() == 'You need to login.'

    resp = auth_client.get('/')
    assert resp.pyquery('main p').text() == 'This is the home page. :)'
