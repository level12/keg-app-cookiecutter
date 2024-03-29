from collections import namedtuple
import threading
import time

from celery.contrib.testing import worker
from keg.db import db

# important to import from .cli so that the commands get attached
from ..cli import {{cookiecutter.project_class}}

TaskResult = namedtuple('TaskResult', 'status, retval, task_id, args, kwargs, einfo, thread_id,'
                        'db_session_id')


def before_start_handler(self, task_id, args, kwargs):
    """
        Setup in conftest.py to receive Task.before_start notifications.
        Needed to set up the app context for testing a celery task.
    """
    task_tracker.task_started()


def on_retry_handler(self, exc, task_id, args, kwargs, einfo):
    """
        Setup in conftest.py to receive Task.on_retry notifications.
        Retries do not return a task result, but the app context needs to
        refresh. Handle the retry, and pop the existing context off, primarily
        to rollback any database operations, before the task restarts.
    """
    task_tracker.task_retry()


def after_return_handler(task, status, retval, task_id, args, kwargs, einfo):
    """
        Setup in conftest.py to receive Task.after_return notifications.

        This function actually gets converted to a method on a Task class, so it has to be a
        function and not a method of TaskTracker.
    """
    result = TaskResult(status, retval, task_id, args, kwargs, einfo, threading.get_ident(),
                        id(db.session))
    task_tracker.task_returned(task.name, result)


class CeleryTaskFailure(Exception):
    pass


class TaskTracker:
    """
        Is used when doing Celery integration testing to wait for a specific task to be processed
        before continuing with testing.

        Example:
            from myapp.celery.tasks import save_db_record

            def some_test(self, celery_worker):
                task_tracker.reset()
                save_db_record.delay(1)
                task_tracker.wait_for('myapp.celery.tasks.save_db_record')
                assert ents.DbRecord.count == 1
    """
    def __init__(self):
        # Don't call reset here, even though the variable assignment is the same.  A reset
        # in the constructor causes the connection to RabbitMQ to be established before
        # it has application-level configuration applied, which means we aren't connecting to the
        # RabbitMQ server we think we are.
        self.app = None
        self.current_app_ctx = None
        self.task_results = {}
        self.slept = 0

    def reset(self):
        self.task_results = {}
        self.slept = 0

    def push_app_context(self):
        self.current_app_ctx = self.app.app_context()
        self.current_app_ctx.push()

    def pop_app_context(self):
        if self.current_app_ctx is not None:
            self.current_app_ctx.pop()
            self.current_app_ctx = None

    def task_started(self):
        self.push_app_context()

    def task_retry(self):
        self.pop_app_context()

    def task_returned(self, task_name, result):
        self.pop_app_context()
        self.task_results[task_name] = result

    def wait_for(self, dotted_task, throw_failure=True, reset_after=True):
        try:
            while dotted_task not in self.task_results:
                assert self.slept <= 40, 'waited too long for task to complete'
                time.sleep(.05)
                self.slept += 1

            result = self.task_results[dotted_task]
            if result.status != 'SUCCESS' and throw_failure:
                raise CeleryTaskFailure(result)
            return result
        finally:
            if reset_after:
                self.reset()


task_tracker = TaskTracker()


class TestWorkController(worker.TestWorkController):
    def on_start(self, **kwargs):
        """
            The worker that is created using Celery pytest fixtures.  It's started in a separate
            thread and that causes problems with the app not being initialized, so we make sure
            to initialize it here.
        """
        super().on_start(**kwargs)
        task_tracker.app = {{cookiecutter.project_class}}.testing_prep()
