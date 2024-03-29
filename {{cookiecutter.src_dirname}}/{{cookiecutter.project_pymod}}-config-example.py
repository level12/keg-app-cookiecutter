from {{cookiecutter.project_pymod}}.celery.config import celery_config

DEFAULT_PROFILE = 'DevProfile'


class DevProfile:
    # Secret key for Flask -- CHANGE THIS!
    SECRET_KEY = 'abc123'

    # Examples:
    #   Socket based, no pass: postgresql://USER@:5433/{{cookiecutter.project_dashed}}
    #   TCP/IP based & matches docker-compose: postgresql://postgres@127.0.0.1:12432/{{cookiecutter.project_dashed}}
    SQLALCHEMY_DATABASE_URI = '{{cookiecutter.sa_db_uri_prefix.rstrip("/")}}/{{cookiecutter.project_dashed}}'

    # These are used for creating an initial developer user following database init
    DEVELOPER_NAME = '{{cookiecutter.developer_name}}'
    DEVELOPER_EMAIL = '{{cookiecutter.developer_email}}'
    DEVELOPER_PASSWORD = '{{cookiecutter.developer_password}}'

    MAIL_DEFAULT_SENDER = '{{cookiecutter.developer_email}}'
    MAIL_SUPPRESS_SEND = True

    KEG_LOG_SYSLOG_ENABLED = False

    # Needed by at least KegAuth for sending emails from the command line
    SERVER_NAME = 'localhost:5000'

    CELERY = celery_config(broker_url='amqp://guest@localhost:12672//')


class TestProfile:
    SQLALCHEMY_DATABASE_URI = '{{cookiecutter.sa_db_uri_prefix.rstrip("/")}}/{{cookiecutter.project_dashed}}-tests'

    # Make tests faster
    PASSLIB_CRYPTCONTEXT_KWARGS = dict(schemes=['plaintext'])

    # Mail related tests need to have this set, even though actual email is not generated.
    MAIL_DEFAULT_SENDER = '{{cookiecutter.developer_email}}'

    CELERY = celery_config(broker_url='amqp://guest@localhost:12672//', queue_name='__tests__')

    # When using `py.test --db-restore ...` this setting tells us what the backup files names look
    # like.  See {{cookiecutter.project_pymod}}.libs.db.testing_db_restore() for more details.
    # Use ./ansible/db-backup.yaml to create these files and view the readme for more information.
    # DB_RESTORE_SQL_FPATH = '/tmp/{{cookiecutter.project_dashed}}-prod-{}.sql'
    # DB_RESTORE_SQL_FPATH = '/tmp/{{cookiecutter.project_dashed}}-beta-{}.sql'
    DB_RESTORE_SQL_FPATH = '/tmp/test-{}.sql'
