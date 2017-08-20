from keg_auth.testing import AuthTests

from {{cookiecutter.project_namespace}}.model import entities as ents


class TestAuthIntegration(AuthTests):
    user_ent = ents.User
    protected_url = '/protected-example'
