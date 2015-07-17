from __future__ import unicode_literals

DEFAULT_PROFILE = 'DevProfile'


class DevProfile(object):
    # secret key for Flask
    SECRET_KEY = ''

    DEVELOPER_NAME = '{{cookiecutter.developer_name}}'
    DEVELOPER_EMAIL = '{{cookiecutter.developer_email}}'
    KEG_EMAIL_OVERRIDE_TO = DEVELOPER_EMAIL


class TestProfile(object):
    pass
