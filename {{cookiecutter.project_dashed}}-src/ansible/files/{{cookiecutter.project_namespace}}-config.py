# flake8: noqa
DEFAULT_PROFILE = 'DeployedProfile'

{% raw %}
class DeployedProfile(object):
    SECRET_KEY = '{{app_flask_secret_key}}'

    SQLALCHEMY_DATABASE_URI = 'postgresql://{{app_db_user}}:{{app_db_pass}}' \
        '@{{app_db_host}}/{{app_db_name}}'

    SENTRY_DSN = '{{pyapp3_sentry_dsn}}'
    SENTRY_ENVIRONMENT = '{{ app_environment }}'

    KEG_KEYRING_ENABLE = False

    # Turn log messages into a JSON string that syslog and/or log aggregators like Loggly will
    # parse.
    KEG_LOG_SYSLOG_JSON = True

    MAIL_DEFAULT_SENDER = 'devteam@level12.io'
    MAIL_DEBUG = False

    CELERY_ALIVE_URL = '{{ app_celery_alive_url }}'
    CELERY = {
        'broker_url': 'amqp://{{ app_rabbitmq_user }}:{{ app_rabbitmq_pass }}@localhost:5672/'
            '{{ app_rabbitmq_vhost }}',
        # Recycle workers at reasonable interval to work around possible memory leaks.
        'worker_max_tasks_per_child': 2000,
    }

    # Needed by at least KegAuth for sending emails from the command line
    SERVER_NAME = '{{ nginx_vhost_server_name }}'
    # This is important so that generated auth related URLS are secure.  We have an SSL redirect
    # but by the time that would fire, the key would have already been sent in the URL.
    PREFERRED_URL_SCHEME = 'https'
{% endraw %}
