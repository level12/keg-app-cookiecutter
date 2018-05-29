
from keg import Keg

from {{cookiecutter.project_namespace}} import extensions
from {{cookiecutter.project_namespace}}.views import blueprints


class {{cookiecutter.project_class}}(Keg):
    import_name = '{{cookiecutter.project_namespace}}'
    use_blueprints = blueprints
    db_enabled = True

    def on_init_complete(self):
        extensions.auth_manager.init_app(self)
        extensions.csrf.init_app(self)
        extensions.flask_mail.init_app(self)
        extensions.bootstrap.init_app(self)

        if self.config.get('SENTRY_DSN'):
            extensions.sentry.init_app(self)
