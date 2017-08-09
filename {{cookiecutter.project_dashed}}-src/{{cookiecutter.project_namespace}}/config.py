
class DefaultProfile(object):
    """
        These values will apply to all configuration profiles.
    """
    # It's tempting to turn this off to avoid the warning, but if you are storing passwords
    # in your settings, leave this enabled and setup a keyring.  See the app's keyring related
    # commands for help.
    KEG_KEYRING_ENABLE = True


class TestProfile(object):
    KEG_KEYRING_ENABLE = False
    # These settings reflect what is needed in CI.  For local development, use
    # {{cookiecutter.project_namespace}}-config.py to override.
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost/postgres'
