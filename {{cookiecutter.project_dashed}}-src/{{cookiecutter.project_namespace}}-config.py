
DEFAULT_PROFILE = 'DevProfile'


class DevProfile(object):
    # Secret key for Flask -- CHANGE THIS!
    SECRET_KEY = 'abc123'

    # TODO: are these needed?  If so, add comment for where they are used.
    DEVELOPER_NAME = '{{cookiecutter.developer_name}}'
    DEVELOPER_EMAIL = '{{cookiecutter.developer_email}}'

    MAIL_DEFAULT_SENDER = '{{cookiecutter.developer_email}}'

    # Needed by at least KegAuth for sending emails from the command line
    SERVER_NAME = 'localhost:5000'


class TestProfile(object):
    """ Uncomment these as needed """
    # SQLALCHEMY_DATABASE_URI = 'postgresql://user:pass@localhost/test'

    # CELERY = {
    #     # This should be for the docker container setup in the CircleCI config.
    #     'broker_url': 'amqp://guest@localhost:5672//',
    #     # Celery integration tests should use a different queue.
    #     'task_default_queue': '__tests__',
    # }
