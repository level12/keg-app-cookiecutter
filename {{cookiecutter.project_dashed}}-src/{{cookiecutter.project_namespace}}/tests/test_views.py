import flask
import flask_webtest as webtest
from keg_auth.testing import ViewTestBase as AuthViewBase, AuthTestApp

from {{cookiecutter.project_namespace}}.model import entities


class PublicViewBase(object):

    @classmethod
    def setup_class(cls):
        # anonymous user
        cls.ta = webtest.TestApp(flask.current_app)


class TestPublic(PublicViewBase):

    def test_home(self):
        resp = self.ta.get('/')
        assert resp.text == 'Hello World from {{cookiecutter.project_name}}!'

    def test_ping(self):
        resp = self.ta.get('/ping')
        assert resp.text == '{{cookiecutter.project_namespace}} ok'

    def test_hello(self):
        resp = self.ta.get('/hello')
        assert 'Hello World!' in resp

        resp = self.ta.get('/hello/foo')
        assert 'Hello foo!' in resp


class TestProtectedExample(AuthViewBase):
    def test_get_with_user(self):
        resp = self.client.get('/protected-example', status=200)
        assert resp.text == 'hi'

    def test_get_without_user(self):
        client = webtest.TestApp(flask.current_app)
        resp = client.get('/protected-example', status=302)
        assert 'login' in resp.location


class TestPermissionExample(AuthViewBase):
    permissions = 'app-permission'

    def test_get_with_authorized_user(self):
        resp = self.client.get('/permission-example', status=200)
        assert resp.text == 'permission-example'

    def test_get_with_unauthorized_user(self):
        user = entities.User.testing_create()
        client = AuthTestApp(flask.current_app, user=user)
        client.get('/permission-example', status=403)

    def test_get_without_user(self):
        client = webtest.TestApp(flask.current_app)
        resp = client.get('/permission-example', status=302)
        assert 'login' in resp.location


class TestBlogCrud(AuthViewBase):
    def test_add(self):
        resp = self.client.get('/blog-posts/add')

        resp.form['title'] = 'test adding a blog post'
        resp.form['posted_utc'] = '2018-06-01 12:00:00'
        resp = resp.form.submit()
        assert resp.status_code == 302
        assert resp.location.endswith('/blog-posts')
        assert resp.flashes == [('success', 'Successfully created Blog Post')]

        assert entities.Blog.get_by(title='test adding a blog post')

    def test_edit(self):
        obj = entities.Blog.testing_create()

        resp = self.client.get('/blog-posts/{}/edit'.format(obj.id))
        assert resp.form['title'].value == obj.title
        resp.form['title'] = 'test editing a blog post'
        resp = resp.form.submit()

        assert resp.status_code == 302
        assert resp.location.endswith('/blog-posts')
        assert resp.flashes == [('success', 'Successfully modified Blog Post')]
        assert entities.Blog.get_by(title='test editing a blog post')

    def test_not_found(self):
        self.client.get('/blog-posts/999999/edit', status=404)
        self.client.get('/blog-posts/999999/delete', status=404)

    def test_delete(self):
        obj_id = entities.Blog.testing_create().id

        resp = self.client.get('/blog-posts/{}/delete'.format(obj_id))

        assert resp.status_code == 302
        assert resp.location.endswith('/blog-posts')
        assert resp.flashes == [('success', 'Successfully removed Blog Post')]

        assert not entities.Blog.query.get(obj_id)

    def test_list(self):
        entities.Blog.testing_create()
        resp = self.client.get('/blog-posts')
        assert 'datagrid' in resp

    def test_list_export(self):
        entities.Blog.testing_create()
        resp = self.client.get('/blog-posts?export_to=xls')
        assert resp.content_type == 'application/vnd.ms-excel'
