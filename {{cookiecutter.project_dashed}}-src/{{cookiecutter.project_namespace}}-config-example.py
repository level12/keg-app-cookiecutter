
DEFAULT_PROFILE = 'DevProfile'


class DevProfile(object):
    # Secret key for Flask -- CHANGE THIS!
    SECRET_KEY = 'abc123'

    # Examples:
    #   Socket based, no pass: postgresql://USER@:5433/{{cookiecutter.project_namespace}}
    #   TCP/IP based: postgresql://USER:PASS@localhost/{{cookiecutter.project_namespace}}
    SQLALCHEMY_DATABASE_URI = '{{cookiecutter.sa_db_uri_prefix.rstrip("/")}}/{{cookiecutter.project_namespace}}'

    # TODO: are these needed?  If so, add comment for where they are used.
    DEVELOPER_NAME = '{{cookiecutter.developer_name}}'
    DEVELOPER_EMAIL = '{{cookiecutter.developer_email}}'

    MAIL_DEFAULT_SENDER = '{{cookiecutter.developer_email}}'

    KEG_LOG_SYSLOG_ENABLED = False

    # Needed by at least KegAuth for sending emails from the command line
    SERVER_NAME = 'localhost:5000'

    CELERY = {
        # Local rabbitmq server
        'broker_url': 'amqp://guest@localhost:5672//',
    }


class TestProfile(object):
    SQLALCHEMY_DATABASE_URI = '{{cookiecutter.sa_db_uri_prefix.rstrip("/")}}/test'

    # Make tests faster
    PASSLIB_CRYPTCONTEXT_KWARGS = dict(schemes=['plaintext'])

    # silence warnings
    KEG_KEYRING_ENABLE = False

    # Mail related tests need to have this set, even though actual email is not generated.
    MAIL_DEFAULT_SENDER = '{{cookiecutter.developer_email}}'

    CELERY = {
        # Local rabbitmq server
        'broker_url': 'amqp://guest@localhost:5672//',
        # Celery integration tests should use a different queue in case we have Celery workers
        # running in development and happen to run tests at the same time.
        'task_default_queue': '__tests__',
    }

    # When using `py.test --db-restore ...` this setting tells us what the backup files names look
    # like.  See {{cookiecutter.project_namespace}}.libs.db.testing_db_restore() for more details.
    # Use ./ansible/db-backup.yaml to create these files and view the readme for more information.
    # DB_RESTORE_SQL_FPATH = '/tmp/{{cookiecutter.project_namespace}}-prod-{}.sql'
    # DB_RESTORE_SQL_FPATH = '/tmp/{{cookiecutter.project_namespace}}-beta-{}.sql'
    DB_RESTORE_SQL_FPATH = '/tmp/test-{}.sql'
