import time
import logging
import requests

from {{cookiecutter.project_namespace}}.celery.app import celery_app as app

log = logging.getLogger(__name__)


@app.task
def error():
    raise ValueError('celery error task')


@app.task
def ping():
    log.info('ping-pong')
    return time.time()


@app.task(bind=True, max_retries=10)
def ping_url(self, url, retry_wait_secs=1):
    log.info('pinging URL: %s', url)

    try:
        requests.get(url)
    except requests.RequestException:
        log.exception('ping_url() encountered an exception')

    raise self.retry(countdown=retry_wait_secs)
