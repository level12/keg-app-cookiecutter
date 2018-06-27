from time import sleep

from keg.testing import CLIBase
import mock

import {{cookiecutter.project_namespace}}.celery.tasks as tasks
from {{cookiecutter.project_namespace}}.celery.testing import task_tracker
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
        assert ents.User.query.filter_by(is_superuser=True).count() == 0

    def test_add_superuser(self):
        self.invoke('auth', 'create-superuser', 'foo@bar.com', 'Foo Bar')
        assert ents.User.query.count() == 1
        assert ents.User.query.filter_by(is_superuser=True).count() == 1


class TestCelerySetup:

    def setup(self):
        task_tracker.reset()

    @mock.patch('{{cookiecutter.project_namespace}}.celery.app.db', autospec=True, spec_set=True)
    def test_removed_ok(self, m_db, celery_session_worker):
        """ The DB session needs to be removed when every task is finished. """

        tasks.ping.delay()

        # Wait for the task to complete in a different thread.
        task_tracker.wait_for('{{cookiecutter.project_namespace}}.celery.tasks.ping')
        # Cleanup is sometimes not complete at this point, need to sleep a minimal amount more
        sleep(0.3)

        m_db.session.remove.assert_called_once_with()

    @mock.patch('{{cookiecutter.project_namespace}}.celery.app.db', autospec=True, spec_set=True)
    def test_removed_error(self, m_db, celery_session_worker):
        """ DB session removal needs to work for exceptions too. """

        tasks.error.delay()

        # Wait for the task to complete in a different thread.
        task_tracker.wait_for('{{cookiecutter.project_namespace}}.celery.tasks.error',
                              throw_failure=False)
        # Cleanup is sometimes not complete at this point, need to sleep a minimal amount more
        sleep(0.3)

        m_db.session.remove.assert_called_once_with()


class TestDBCli(CLIBase):

    @mock.patch('{{cookiecutter.project_namespace}}.cli.db.lib_db.PostgresBackup', autospec=True, spec_set=True)
    def test_backup(self, m_PostgresBackup):
        # set "errors" to nothing
        m_PostgresBackup.return_value.run.return_value = []
        result = self.invoke('db', 'backup', 'sql')
        assert 'backup finished\n' == result.output

    @mock.patch('{{cookiecutter.project_namespace}}.cli.db.lib_db.PostgresRestore', autospec=True, spec_set=True)
    def test_restore(self, PostgresRestore):
        # set "errors" to nothing
        PostgresRestore.return_value.run.return_value = []
        # The restore doesn't work b/c of the mock, but we have to feed it a path that exists.
        result = self.invoke('db', 'restore', '/tmp')
        assert 'restore finished\n' == result.output
