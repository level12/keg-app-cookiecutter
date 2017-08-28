# flake8: noqa
DEFAULT_PROFILE = 'DeployedProfile'

{% raw %}
class DeployedProfile(object):
    SECRET_KEY = '{{app_flask_secret_key}}'

    SQLALCHEMY_DATABASE_URI = 'postgresql://{{app_db_user}}:{{app_db_pass}}' \
        '@{{app_db_host}}/{{app_db_name}}'

    SENTRY_DSN = '{{app_sentry_dsn}}'

    KEG_KEYRING_ENABLE = False
    KEG_LOG_SYSLOG_JSON = True


    MAIL_DEFAULT_SENDER = ''

    # Needed by at least KegAuth for sending emails from the command line
    SERVER_NAME = '{{ nginx_vhost_server_name }}'
{% endraw %}
