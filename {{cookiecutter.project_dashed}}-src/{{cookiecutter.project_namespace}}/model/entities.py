import logging

from keg.db import db
from keg_elements.db.mixins import DefaultColsMixin, MethodsMixin
import keg_auth
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.hybrid import hybrid_property

from ..extensions import auth_entity_registry
from ..libs.model import EntityMixin, tc_relation

log = logging.getLogger(__name__)

# Default cascade setting for parent/child relationships.  Should get set on parent side.
# Docs: https://l12.io/sa-parent-child-relationship-config
_rel_cascade = 'all, delete-orphan'


class EntityMixin(DefaultColsMixin, MethodsMixin):
    pass


@auth_entity_registry.register_user
class User(db.Model, keg_auth.UserEmailMixin, keg_auth.UserMixin, EntityMixin):
    """ Make sure EntityMixin is after UserMixin or testing_create() is wrong.  """
    __tablename__ = 'users'

    name = sa.Column(sa.Unicode(250), nullable=False)
    settings = sa.Column(JSONB)


@auth_entity_registry.register_permission
class Permission(db.Model, keg_auth.PermissionMixin, EntityMixin):
    __tablename__ = 'permissions'

    def __repr__(self):
        return '<Permission id={} token={}>'.format(self.id, self.token)


@auth_entity_registry.register_bundle
class Bundle(db.Model, keg_auth.BundleMixin, EntityMixin):
    __tablename__ = 'bundles'


@auth_entity_registry.register_group
class Group(db.Model, keg_auth.GroupMixin, EntityMixin):
    __tablename__ = 'groups'
