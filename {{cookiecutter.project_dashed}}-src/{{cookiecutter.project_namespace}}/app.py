from flask_bootstrap import Bootstrap
from flask_mail import Mail
from keg import Keg
import keg_auth
from flask_wtf.csrf import CSRFProtect
from raven.contrib.flask import Sentry

from {{cookiecutter.project_namespace}}.views import blueprints

csrf = CSRFProtect()
mail_ext = Mail()
sentry = Sentry()


class AuthManager(keg_auth.AuthManager):

    def create_user_cli(self, email, extra_args):
        """ A thin layer between the cli and `create_user()` to transform the cli args
            into what the User entity expects for fields.

            For example, if you had a required `name` field on your User entity, then you could do
            something like::

                $ yourkegapp auth create-user john.smith@example.com "John Smith"

            Then this method would get overriden in a sub-class like:

                def create_user_cli(self, email, extra_args):
                    user_kwargs = dict(email=email, name=extra_args[0])
                    return self.create_user(user_kwargs)
        """
        # Our user model takes a required name field
        assert len(extra_args) == 1
        user_kwargs = dict(email=email, name=extra_args[0])
        return self.create_user(user_kwargs)


_endpoints = {'after-login': 'public.home'}
auth_manager = AuthManager(mail_ext, endpoints=_endpoints)


class {{cookiecutter.project_class}}(Keg):
    import_name = '{{cookiecutter.project_namespace}}'
    use_blueprints = blueprints
    db_enabled = True

    def on_init_complete(self):
        auth_manager.init_app(self)
        csrf.init_app(self)
        mail_ext.init_app(self)
        Bootstrap(self)

        if self.config.get('SENTRY_DSN'):
            sentry.init_app(self)
