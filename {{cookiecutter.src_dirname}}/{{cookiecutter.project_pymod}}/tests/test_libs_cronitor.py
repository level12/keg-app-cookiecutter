from unittest import mock

import pytest

from ..libs.cronitor import cronitor_job, get_monitor
from ..libs.testing import app_config


@mock.patch('{{cookiecutter.project_pymod}}.libs.cronitor.Monitor', autospec=True, spec_set=True)
def test_get_monitor(m_monitor):
    with app_config(CRONITOR_MONITOR_SUFFIX='{{cookiecutter.project_pymod}}-test'):
        get_monitor('no-worries')
    assert m_monitor.mock_calls == [mock.call('no-worries-{{cookiecutter.project_pymod}}-test')]


@mock.patch('{{cookiecutter.project_pymod}}.libs.cronitor.get_monitor', autospec=True, spec_set=True)
class TestCronitorJob:
    def test_success(self, m_get_monitor):
        with cronitor_job('test', True):
            pass
        assert m_get_monitor.mock_calls == [
            mock.call('test'),
            mock.call().ping(state='run'),
            mock.call().ping(state='complete'),
        ]

    def test_fail(self, m_get_monitor):
        class MyException(Exception):
            pass

        with pytest.raises(MyException):
            with cronitor_job('test', True):
                raise MyException()

        assert m_get_monitor.mock_calls == [
            mock.call('test'),
            mock.call().ping(state='run'),
            mock.call().ping(state='fail'),
        ]

    def test_no_ping(self, m_get_monitor):
        with cronitor_job('test', False):
            pass

        assert not m_get_monitor.called
