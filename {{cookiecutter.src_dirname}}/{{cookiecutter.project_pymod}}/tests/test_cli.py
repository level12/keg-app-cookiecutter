from unittest import mock

from keg.testing import CLIBase

from ..model import entities as ents


class TestCLI(CLIBase):
    def setup_method(self):
        ents.User.delete_cascaded()

    def test_add_user(self):
        self.invoke('auth', 'create-user', 'foo@bar.com', 'Foo Bar')
        assert ents.User.query.count() == 1
        assert ents.User.query.filter_by(is_superuser=True).count() == 0

    def test_add_superuser(self):
        self.invoke('auth', 'create-user', '--as-superuser', 'foo@bar.com', 'Foo Bar')
        assert ents.User.query.count() == 1
        assert ents.User.query.filter_by(is_superuser=True).count() == 1


class TestDBCli(CLIBase):
    @mock.patch('{{cookiecutter.project_pymod}}.cli.db.lib_db.PostgresBackup', autospec=True, spec_set=True)
    def test_backup(self, m_PostgresBackup):
        # set "errors" to nothing
        m_PostgresBackup.return_value.run.return_value = []
        result = self.invoke('db', 'backup', 'sql')
        assert 'backup finished\n' == result.output

    @mock.patch('{{cookiecutter.project_pymod}}.cli.db.lib_db.PostgresRestore', autospec=True, spec_set=True)
    def test_restore(self, PostgresRestore):
        # set "errors" to nothing
        PostgresRestore.return_value.run.return_value = []
        # The restore doesn't work b/c of the mock, but we have to feed it a path that exists.
        result = self.invoke('db', 'restore', '/tmp')
        assert 'restore finished\n' == result.output
