
class DefaultProfile(object):
    """
        These values will apply to all configuration profiles.
    """
    # It's tempting to turn this off to avoid the warning, but if you are storing passwords
    # in your settings, leave this enabled and setup a keyring.  See the app's keyring related
    # commands for help.
    KEG_KEYRING_ENABLE = True

    # Used in at least KegAuth email templates
    SITE_NAME = '{{cookiecutter.project_name}}'
    # Used in at least KegAuth email subject lines
    SITE_ABBR = '{{cookiecutter.project_name}}'

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestProfile(object):
    # These settings reflect what is needed in CI.  For local development, use
    # {{cookiecutter.project_namespace}}-config.py to override.
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost/postgres'

    # Make tests faster
    PASSLIB_CRYPTCONTEXT_KWARGS = dict(schemes=['plaintext'])

    # silence warnings
    KEG_KEYRING_ENABLE = False

    # Mail related tests need to have this set, even though actual email is not generated.
    MAIL_DEFAULT_SENDER = '{{cookiecutter.developer_email}}'

    CELERY = {
        # This should be for the docker container setup in the CircleCI config.
        'broker_url': 'amqp://guest@localhost:5672//',
    }
