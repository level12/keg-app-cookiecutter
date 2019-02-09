import flask.json
from keg import Keg
import keg.db

from {{cookiecutter.project_namespace}} import extensions, grids, navigation
from {{cookiecutter.project_namespace}}.libs.db import testing_db_restore
import {{cookiecutter.project_namespace}}.libs.json as _app_json
from {{cookiecutter.project_namespace}}.views import blueprints
from {{cookiecutter.project_namespace}}.grids import Grid


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
        extensions.auth_manager.grid_cls = Grid
        extensions.csrf.init_app(self)
        extensions.mail.init_app(self)
        extensions.bootstrap.init_app(self)

        if self.config.get('SENTRY_DSN'):
            extensions.sentry.init_app(self)

        navigation.init_navigation(self)

        grids.Grid.manager.init_db(keg.db.db)
        grids.Grid.manager.init_app(self)


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
