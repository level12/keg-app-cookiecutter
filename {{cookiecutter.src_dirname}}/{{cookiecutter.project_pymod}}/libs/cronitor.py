import contextlib

import cronitor as _cronitor
import flask
from cronitor.monitor import Monitor


class Cronitor:
    def init_app(self, app):
        _cronitor.api_key = app.config['CRONITOR_API_KEY']
        _cronitor.environment = app.config['CRONITOR_ENVIRONMENT']
        app.cronitor = _cronitor


def get_monitor(key: str) -> Monitor:
    monitor_suffix = flask.current_app.config['CRONITOR_MONITOR_SUFFIX']
    return Monitor(f'{key}-{monitor_suffix}')


@contextlib.contextmanager
def cronitor_job(key: str, do_ping: bool):
    if not do_ping:
        yield
    else:
        monitor = get_monitor(key)
        monitor.ping(state='run')
        try:
            yield
            monitor.ping(state='complete')
        except Exception:
            monitor.ping(state='fail')
            raise
