
DEFAULT_PROFILE = 'DevProfile'


class DevProfile(object):
    # Secret key for Flask -- CHANGE THIS!
    SECRET_KEY = 'abc123'

    # Examples:
    #   Socket based, no pass: postgresql://USER@:5433/{{cookiecutter.project_namespace}}
    #   TCP/IP based: postgresql://USER:PASS@localhost/{{cookiecutter.project_namespace}}
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/{{cookiecutter.project_namespace}}.db'

    # TODO: are these needed?  If so, add comment for where they are used.
    DEVELOPER_NAME = '{{cookiecutter.developer_name}}'
    DEVELOPER_EMAIL = '{{cookiecutter.developer_email}}'

    MAIL_DEFAULT_SENDER = '{{cookiecutter.developer_email}}'

    # Needed by at least KegAuth for sending emails from the command line
    SERVER_NAME = 'localhost:5000'

    CELERY = {
        # Local rabbitmq server
        'broker_url': 'amqp://guest@localhost:5672//',
    }


class TestProfile(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/{{cookiecutter.project_namespace}}-test.db'

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
