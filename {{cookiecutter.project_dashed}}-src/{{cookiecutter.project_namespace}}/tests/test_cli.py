from __future__ import absolute_import
from __future__ import unicode_literals

from pathlib import Path
from scripttest import TestFileEnvironment

_output_dir = Path(__file__).parent.joinpath('.scriptest-output').__str__()


class CLIBase(object):

    @classmethod
    def setup_class(cls):
        # todo: allow configuration of the environment to test with
        cls.env = TestFileEnvironment(_output_dir)

    def run(self, *args):
        return self.env.run('{{cookiecutter.project_namespace}}', '--profile', 'Test', *args)


class TestCLI(CLIBase):

    def test_hello(self):
        result = self.run('hello')
        assert 'Hello World from {{cookiecutter.project_name}}!\n' == result.stdout

        result = self.run('hello', '--name', 'Foo')
        assert 'Hello Foo from {{cookiecutter.project_name}}!\n' == result.stdout

