import contextlib
import keg
import logging
import requests

from .app import celery_app as app

log = logging.getLogger(__name__)


def cronitor_ping(config_key, endpoint, alive=True):
    if not alive:
        # This is to support a common pattern in our CLI commands where we may or may not want to
        # ping cronitor based on a CLI flag. Keeps us from scattering "if" statements everywhere.
        return
    monitor_key = keg.current_app.config[config_key]
    env = keg.current_app.config['CRONITOR_ENV']
    url = f'https://cronitor.link/{monitor_key}/{endpoint}?env={env}'
    ping_url.apply_async((url,), priority=1)


@contextlib.contextmanager
def cronitor_job(config_key, alive):
    _last_endpoint = 'complete'

    def last_ping(endpoint):
        # `ok` is used to "reset" a cronitor once it's started.  It's a way to finish a cronitor run
        # without using the "complete" endpoint.  E.g. run a job hourly that checks a mail server
        # for incoming mail that only arrives once a day.  In this case, you'd set the cronitor
        # up to be scheduled every hour but require it to complete once a day.  You'd set `ok`
        # every time you run and the mail isn't there and leave the default of `complete` when
        # you process the email once a day.
        #
        # `fail` used to fail the job without requiring an exception to be thrown.
        assert endpoint in ('ok', 'fail')
        nonlocal _last_endpoint
        _last_endpoint = endpoint

    cronitor_ping(config_key, 'run', alive)
    try:
        yield last_ping
        cronitor_ping(config_key, _last_endpoint, alive)
    except Exception:
        cronitor_ping(config_key, 'fail', alive)
        raise


@app.task(bind=True, max_retries=10)
def ping_url(self, url, retry_wait_secs=1):
    log.info('pinging URL: %s', url)

    try:
        requests.get(url, timeout=10)
    except requests.RequestException:
        log.exception('ping_url() encountered an exception')
        raise self.retry(countdown=retry_wait_secs)


@app.task
def say(msg):
    log.info(f'say: {msg}')
