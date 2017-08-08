import flask
from flask.ext.webtest import TestApp


class ViewBase(object):

    @classmethod
    def setup_class(cls):
        # anonymous user
        cls.ta = TestApp(flask.current_app)


class TestPublic(ViewBase):

    def test_home(self):
        resp = self.ta.get('/')
        assert resp.text == 'Hello World from {{cookiecutter.project_name}}!'

    def test_ping(self):
        resp = self.ta.get('/ping')
        assert resp.text == '{{cookiecutter.project_namespace}} ok'
