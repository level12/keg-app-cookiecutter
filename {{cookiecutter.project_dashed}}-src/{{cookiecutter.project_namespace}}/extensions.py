
"""
    We init the extensions outside of .app to make less likely to be in an import loop.
"""
from flask_bootstrap import Bootstrap
from flask_mail import Mail as FlaskMail
from flask_wtf.csrf import CSRFProtect
from keg_auth import AuthManager, AuthMailManager, AuthEntityRegistry

from {{cookiecutter.project_namespace}}.libs.grids import Grid
from {{cookiecutter.project_namespace}}.libs.sentry import Sentry

permissions = (
    'app-permission',
    'auth-manage',
)

mail = FlaskMail()
auth_mail_manager = AuthMailManager(mail)
auth_entity_registry = AuthEntityRegistry()

_app_endpoints = {'after-login': 'auth.user'}
auth_manager = AuthManager(
    mail_manager=auth_mail_manager,
    endpoints=_app_endpoints,
    permissions=permissions,
    entity_registry=auth_entity_registry,
    grid_cls=Grid,
)

csrf = CSRFProtect()

sentry = Sentry()

bootstrap = Bootstrap()
