
"""
    We init the extensions outside of .app to make less likely to be in an import loop.
"""
from flask_bootstrap import Bootstrap
from flask_mail import Mail as FlaskMail
from flask_wtf.csrf import CSRFProtect
from keg_auth import AuthManager
from keg_elements.sentry import SentryClient
from raven.contrib.flask import Sentry

permissions = (
    'app-permission',
    'auth-manage',
)

mail = FlaskMail()

_app_endpoints = {'after-login': 'public.home'}
auth_manager = AuthManager(mail, endpoints=_app_endpoints, permissions=permissions)

csrf = CSRFProtect()

sentry = Sentry(client_cls=SentryClient)

bootstrap = Bootstrap()
