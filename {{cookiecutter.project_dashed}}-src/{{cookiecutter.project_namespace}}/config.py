import flask


class DefaultProfile(object):
    """
        These values will apply to all configuration profiles.
    """
    # Used in at least email templates
    SITE_NAME = '{{cookiecutter.project_name}}'
    # Used in at least email subject lines
    SITE_ABBR = '{{cookiecutter.project_name}}'

    # Used at least by Keg Auth templates to know what to extend
    BASE_TEMPLATE = 'base-page.html'

    # Used by Keg Auth CLI to determine what arguments to require for create-user
    KEGAUTH_CLI_USER_ARGS = ['name', 'email']

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # For PGSQL applications, can be removed for other db platforms
    SQLALCHEMY_ENGINE_OPTIONS = {
        'json_serializer': flask.json.dumps,
        'json_deserializer': flask.json.loads,
    }

    SENTRY_USER_ATTRS = ['email', 'name']


class TestProfile(object):
    # These settings reflect what is needed in CI.  For local development, use
    # {{cookiecutter.project_namespace}}-config.py to override.
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost/postgres'

    # Make tests faster
    PASSLIB_CRYPTCONTEXT_KWARGS = dict(schemes=['plaintext'])

    # Mail related tests need to have this set, even though actual email is not generated.
    MAIL_DEFAULT_SENDER = 'devteam+i-better-not-get-email-from-these-tests@level12.io'

    CELERY = {
        # This should be for the docker container setup in the CircleCI config.
        'broker_url': 'amqp://guest@localhost:5672//',
    }
