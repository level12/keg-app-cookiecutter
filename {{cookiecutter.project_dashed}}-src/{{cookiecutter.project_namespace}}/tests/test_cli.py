from keg.testing import CLIBase

from {{cookiecutter.project_namespace}}.app import {{cookiecutter.project_class}}


class TestCLI(CLIBase):
    app_cls = {{cookiecutter.project_class}}
    cmd_name = 'hello'

    def test_hello(self):
        result = self.invoke()
        assert 'Hello World from {{cookiecutter.project_name}}!\n' == result.output

        result = self.invoke('--name', 'Foo')
        assert 'Hello Foo from {{cookiecutter.project_name}}!\n' == result.output
