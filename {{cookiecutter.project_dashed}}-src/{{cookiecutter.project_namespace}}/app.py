from keg import Keg
import keg.db

from {{cookiecutter.project_namespace}} import extensions, navigation
from {{cookiecutter.project_namespace}}.libs.db import testing_db_restore
from {{cookiecutter.project_namespace}}.libs.grids import Grid
import {{cookiecutter.project_namespace}}.libs.json as _app_json
from {{cookiecutter.project_namespace}}.auth import blueprints


class {{cookiecutter.project_class}}(Keg):
    import_name = '{{cookiecutter.project_namespace}}'
    use_blueprints = blueprints
    db_enabled = True

    json_encoder = _app_json.JSONEncoder
    json_decoder = _app_json.JSONDecoder

    def db_manager_cls(self):
        return DatabaseManager

    def on_init_complete(self):
        extensions.auth_manager.init_app(self)
        extensions.csrf.init_app(self)
        extensions.mail.init_app(self)
        extensions.bootstrap.init_app(self)

        if self.config.get('SENTRY_DSN'):
            extensions.sentry.init_app(self)

        navigation.init_navigation(self)

        Grid.manager.init_db(keg.db.db)
        Grid.manager.init_app(self)


class DatabaseManager(keg.db.DatabaseManager):
    """
        Customized DB manage to support:
        1) Running tests without clearing the DB schema.  This is used when you want to run
            tests on a database restore + Alembic migration.
    """

    def on_testing_start(self, app):
        if app.config.get('TESTING_DB_RESTORE', False):
            testing_db_restore(app)
        else:
            self.db_init_with_clear()

    def db_init(self):
        super().db_init()
        # If all the developer variables are set, then create our first user.
        try:
            from {{cookiecutter.project_namespace}}.model.entities import User
            User.add(
                name=self.app.config['DEVELOPER_NAME'],
                email=self.app.config['DEVELOPER_EMAIL'],
                password=self.app.config['DEVELOPER_PASSWORD'],
                is_verified=True,
                is_superuser=True,
            )
        except KeyError:
            pass
