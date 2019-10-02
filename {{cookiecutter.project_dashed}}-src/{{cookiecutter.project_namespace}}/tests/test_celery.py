from unittest import mock

from {{cookiecutter.project_namespace}}.celery import tasks
from {{cookiecutter.project_namespace}}.celery.testing import task_tracker


class TestCeleryTasks:

    @mock.patch('{{cookiecutter.project_namespace}}.celery.tasks.log', autospec=True, spec_set=True)
    def test_ping(self, m_log, celery_session_worker):
        task_tracker.reset()
        tasks.ping.delay()

        # Have to wait for the task to complete or we might test for the action before
        # the celery worker can process it.
        task_tracker.wait_for('{{cookiecutter.project_namespace}}.celery.tasks.ping')

        m_log.info.assert_called_once_with('ping-pong')
