from contextlib import contextmanager
from os import path as osp

import keg

import alembic
import alembic.config
from alembic.script import ScriptDirectory

import sqlalchemy as sa

from sqlalchemy.dialects import postgresql


def alembic_config(config=None):
    config = config or alembic.config.Config()
    project_src_dpath = osp.dirname(keg.current_app.root_path)
    script_location = osp.join(project_src_dpath, 'alembic')
    config.set_main_option('script_location', script_location)
    config.set_main_option('bootstrap_app', 'false')
    config.set_main_option('sqlalchemy.url', keg.current_app.config['SQLALCHEMY_DATABASE_URI'])
    return config


def alembic_upgrade(revision):
    alembic_conf = alembic_config()
    alembic.command.upgrade(alembic_conf, revision)


def alembic_apply(revision):
    """
    Stamp the current DB at the "down_revision" of the revision to be applied. Then,
    "upgrade" to the revision requested.
    This should guarantee that only the requested revision is run and nothing it depends on.
    """
    alembic_conf = alembic_config()
    scriptdir = ScriptDirectory.from_config(alembic_conf)
    script = scriptdir.get_revision(revision)
    if script.down_revision is None:
        down_revision = 'base'
    else:
        down_revision = script.down_revision

    alembic.command.stamp(alembic_conf, down_revision)
    alembic.command.upgrade(alembic_conf, revision)


@contextmanager
def alembic_automap_init(alembic_op):
    # Import inside to avoid circular imports.  {{cookiecutter.project_pymod}}.libs.db imports
    # from this file.
    from .db import reflect_db

    # Use the same connection to the DB that the Alembic environment is using so that all of our
    # operations are happening withing the single Alembic-managed transaction.  The goal is that
    # multiple migrations can be ran and all will succeed or fail together.
    conn = alembic_op.get_context().connection
    Base, sa_session = reflect_db(conn)

    try:
        yield Base, sa_session
        # Flush any pending operations in the session.  No need for a commit b/c it wouldn't really
        # apply at the connection level anyway.  See below for details on why.
        sa_session.flush()
    finally:
        # Even though we are sharing the connection/transaction the Alembic environment has setup,
        # closing the session here will not affect the outer Alembic-managed transaction.  This is
        # due to the fact that the connection object maintains subtransactions.  Further reading:
        # http://docs.sqlalchemy.org/en/rel_1_0/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites # noqa
        sa_session.close()


class EnumUpdate:
    """ Update an enum. Example Usage:

        with EnumUpdate(op, 'enum_validation_status') as enum_up:
            enum_up.set_values('unknown', 'invalid', 'valid', 'empire')

            update_map = {'invalid': 'empire'}
            enum_up.alter_column('assignments', 'validation', default='unknown')
            enum_up.alter_column('time_entries', 'validation', update_map)
            enum_up.alter_column('expenses', 'validation', update_map)
    """

    def __init__(self, op, enum_name):
        self.columns = []
        self.enum_name = enum_name
        self.enum_values = None
        self.op = op

    def set_values(self, *values):
        self.enum_values = values

    def alter_column(self, table_name, col_name, update_map=None, default=None, **kwargs):
        if update_map is None and kwargs:
            update_map = kwargs

        self.columns.append((table_name, col_name, default))

        ac_kwargs = {'type_': sa.String,}
        if default:
            ac_kwargs['server_default'] = None

        self.op.alter_column(table_name, col_name, **ac_kwargs)

        if update_map:
            # Required instead of op.execute() so parameters will work, even though SQL injection
            # here is unlikely it will take care of quoting different values for us.
            conn = self.op.get_bind()
            for old_value, new_value in update_map.items():
                sql = sa.text(f'''
                    update {table_name}
                    set {col_name} = :new_value
                    where {col_name} = :old_value
                ''')
                conn.execute(sql, new_value=new_value, old_value=old_value)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if type:
            # We don't handle exceptions, this will cause it to raise
            return

        enum = enum_create(self.op, self.enum_name, *self.enum_values, drop_first=True)

        for table_name, col_name, default in self.columns:
            self.op.alter_column(
                table_name,
                col_name,
                type_=enum,
                existing_type=sa.String,
                postgresql_using='{}::{}'.format(col_name, self.enum_name),
                server_default=default,
            )


def enum_create(op, name, *values, drop_first=False):
    enum = postgresql.ENUM(*values, name=name)
    if drop_first:
        op.execute(f'DROP TYPE IF EXISTS {name}')
    enum.create(op.get_bind())

    return enum
