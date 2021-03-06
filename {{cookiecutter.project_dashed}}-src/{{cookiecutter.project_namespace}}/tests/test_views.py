import flask
import flask_webtest as webtest


class PublicViewBase(object):

    @classmethod
    def setup_class(cls):
        # anonymous user
        cls.ta = webtest.TestApp(flask.current_app)


class TestPublic(PublicViewBase):

    def test_ping(self):
        resp = self.ta.get('/ping')
        assert resp.text == '{{cookiecutter.project_namespace}} ok'
