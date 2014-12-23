from __future__ import unicode_literals


class Default(object):
    """
        apply's to all config profiles
    """
    # It's tempting to turn this off to avoid the warning, but if you are storing passwords
    # in your settings, leave this enabled and setup a keyring.  See the app's keyring related
    # commands for help.
    KEG_KEYRING_ENABLE = True


class Dev(object):
    # secret key for Flask
    SECRET_KEY = ''
    DEVELOPER_EMAIL = '{{cookiecutter.developer_email}}'
