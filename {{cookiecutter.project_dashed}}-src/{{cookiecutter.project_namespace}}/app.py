import flask.json
from keg import Keg
import keg.db

from {{cookiecutter.project_namespace}} import extensions, grids, navigation
from {{cookiecutter.project_namespace}}.libs.db import testing_db_restore
import {{cookiecutter.project_namespace}}.libs.json as _app_json
from {{cookiecutter.project_namespace}}.views import blueprints


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

        grids.Grid.manager.init_db(keg.db.db)
        grids.Grid.manager.init_app(self)


class DatabaseManager(keg.db.DatabaseManager):
    """
        Customized DB manage to support:
        1) Running tests without clearing the DB schema.  This is used when you want to run
            tests on a database restore + Alembic migration.
        2) Setting custom json serialization methods for psycopg2 to prevent issues when trying
            to serlizaze data to JSONB columns, especially data that has datetime fields.

            This code is espcially hacky with the monkey patch and will have to stay that way
            until one or both of these issues are addressed:
            * https://github.com/mitsuhiko/flask-sqlalchemy/issues/166
            * https://github.com/level12/keg/issues/59
    """
    def init_app(self):
        # We need to monkey patch here because Keg/SQLAlchemy don't easily expose the options
        # that get passed to create_engine().
        def apply_pool_defaults(app, options):
            """ Use this func to monkey patch SQLAlchemy.apply_pool_defaults()"""
            # Call the monkey-patched method
            keg.db.KegSQLAlchemy.apply_pool_defaults(self, app, options)

            # JSON serialize/deserialize will use our app's *coders.  They can be customized in
            # {{cookiecutter.project_namespace}}.libs.json
            options['json_serializer'] = flask.json.dumps
            options['json_deserializer'] = flask.json.loads

            # Turn on SA pessimistic disconnect handling:
            # http://docs.sqlalchemy.org/en/latest/core/pooling.html#disconnect-handling-pessimistic
            options['pool_pre_ping'] = True

        # db is the instance of KegSQLAlchemy created in keg.db
        db = keg.db.db
        db.apply_pool_defaults = apply_pool_defaults

        super().init_app()

    def on_testing_start(self, app):
        if app.config.get('TESTING_DB_RESTORE', False):
            testing_db_restore(app)
        else:
            self.db_init_with_clear()
