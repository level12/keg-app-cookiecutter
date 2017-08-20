from keg.testing import CLIBase

from {{cookiecutter.project_namespace}}.model import entities as ents


class TestCLI(CLIBase):

    def setup(self):
        ents.User.delete_cascaded()

    def test_hello(self):
        result = self.invoke('hello')
        assert 'Hello World from {{cookiecutter.project_name}}!\n' == result.output

        result = self.invoke('hello', '--name', 'Foo')
        assert 'Hello Foo from {{cookiecutter.project_name}}!\n' == result.output

    def test_add_user(self):
        self.invoke('auth', 'create-user', 'foo@bar.com', 'Foo Bar')
        assert ents.User.query.count() == 1
