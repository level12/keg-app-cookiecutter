from alembic import context
import keg
from keg.db import db

from {{cookiecutter.project_namespace}}.app import {{cookiecutter.project_class}}

if keg.current_app:
    app = keg.current_app
else:
    app = {{cookiecutter.project_class}}()

    # Get the configuration and ensure that Keg's database has been initialized. We don't run the
    # full ``app.init()`` here because some plugins touch the database as they are setup and in some
    # cases, those tables wont exist if we haven't run the migrations which is what we are trying to
    # do.
    app.init_config(None, False, None)
    app.init_db()

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = db.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = db.get_engines(app)[0][1]

    print("Operating on database at: {}".format(connectable.url))

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
