import flask
import flask_webtest as webtest
from keg_auth.testing import AuthTestApp, ViewTestBase
import pytest

from ..model import entities as ents
from ..libs.testing import mock_patch


# Scope needs to be class level b/c ViewTestBase clears out users in setup_class()
@pytest.fixture(scope='class')
def auth_client(perms=None):
    return AuthTestApp(flask.current_app, user=ents.User.testing_create(permissions=perms))


class TestPublic:
    @classmethod
    def setup_class(cls):
        # anonymous user
        cls.client = webtest.TestApp(flask.current_app)

    def test_ping(self):
        # This only tests the view layer, provided by Keg. Don't use this for cronitor.
        # Refs: https://github.com/level12/keg-app-cookiecutter/issues/130
        resp = self.client.get('/ping')
        assert resp.text == '{{cookiecutter.project_pymod}} ok'

    @mock_patch('{{cookiecutter.project_pymod}}.views.public.ctasks')
    def test_health_check(self, m_ctasks):
        # Use this for cronitor.
        resp = self.client.get('/health-check')
        assert resp.text == '{{cookiecutter.project_pymod}} ok'
        m_ctasks.ping_url.apply_async.assert_called_once_with(('keep-celery-alive',), priority=10)

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


class TestPrivate(ViewTestBase):
    permissions = ('manager',)

    @pytest.mark.parametrize('url,heading', [
        ('/departments', 'Departments'),
        ('/product-categories', 'Product Categories'),
        ('/product-brands', 'Product Brands'),
        ('/products', 'Products'),
    ])
    def test_view_perms(self, url, heading, auth_client):
        # Manager permission required, only authenticated doesn't cut it
        assert auth_client.get(url, status=403)

        resp = self.client.get(url)
        doc = resp.pyquery
        assert doc('h1').text() == heading

    def test_days(self, auth_client):
        resp = auth_client.get('/days')
        doc = resp.pyquery
        assert doc('h1').text() == 'Production Days'


class TestProductionDay(ViewTestBase):
    permissions = ('manager',)

    @classmethod
    def setup_class(cls):
        super().setup_class()

        ents.ProductionDay.delete_cascaded()

        cls.d1_id = ents.Department.testing_create(name='D1').id
        cls.d2_id = ents.Department.testing_create(name='D2').id

        cls.day_id = ents.Day.testing_create(date='2020-08-17').id

        ents.ProductionDay.testing_create(day_id=cls.day_id, product__department_id=cls.d1_id)
        ents.ProductionDay.testing_create(day_id=cls.day_id, product__department_id=cls.d2_id)

    def test_tabs(self):
        resp = self.client.get(f'/production-day/{self.day_id}')
        doc = resp.pyquery
        assert doc('.nav-tabs').text() == 'Summary\nD1\nD2'

    def test_summary(self):

        resp = self.client.get(f'/production-day/{self.day_id}')
        doc = resp.pyquery
        assert doc('h1').text() == 'Production for 2020-08-17'
        sec = doc('section.tab-content')
        assert sec('h2').eq(0).text() == 'D1'
        assert sec('h2').eq(1).text() == 'D2'
        assert sec('tfoot').eq(0)('th,td').text() == 'Totals: 0 0 0 0'

    def test_dept(self):
        url = f'/production-day/{self.day_id}/dept/{self.d1_id}'
        resp = self.client.get(url)
        doc = resp.pyquery
        assert doc('h1').text() == 'Production for 2020-08-17'
        script_text = doc('script').text()
        assert 'frontend.renderApp(' in script_text
        assert f'{url}?json' in script_text

    def test_update_field(self):
        pd = ents.ProductionDay.testing_create()
        pd = ents.ProductionDay.query_for('day', id=pd.id).one()
        pd2 = ents.ProductionDay.testing_create()

        url = '/production-day-update-field'

        assert pd.ordered == 0
        assert pd.add_on == 0

        json = {'id': pd.id, 'fieldName': 'addOn', 'value': 3}
        resp = self.client.post_json(url, json)
        assert resp.status_code == 200

        assert pd.add_on == 3
        assert pd2.add_on == 0
