import datetime as dt
import logging

from keg.db import db
import keg_auth
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.hybrid import hybrid_property

from ..extensions import auth_entity_registry
from ..libs.model import EntityMixin, tc_relation

log = logging.getLogger(__name__)

# Default cascade setting for parent/child relationships.  Should get set on parent side.
# Docs: https://l12.io/sa-parent-child-relationship-config
_rel_cascade = 'all, delete-orphan'


@auth_entity_registry.register_user
class User(db.Model, keg_auth.UserEmailMixin, keg_auth.UserMixin, EntityMixin):
    """ Make sure EntityMixin is after UserMixin or testing_create() is wrong.  """
    __tablename__ = 'auth_users'

    name = sa.Column(sa.Unicode(250), nullable=False)
    settings = sa.Column(JSONB)


@auth_entity_registry.register_permission
class Permission(db.Model, keg_auth.PermissionMixin, EntityMixin):
    __tablename__ = 'auth_permissions'

    def __repr__(self):
        return '<Permission id={} token={}>'.format(self.id, self.token)


@auth_entity_registry.register_bundle
class Bundle(db.Model, keg_auth.BundleMixin, EntityMixin):
    __tablename__ = 'auth_bundles'


@auth_entity_registry.register_group
class Group(db.Model, keg_auth.GroupMixin, EntityMixin):
    __tablename__ = 'auth_groups'


class Department(EntityMixin, db.Model):
    __tablename__ = 'departments'
    __upsert_index_elements__ = ('name',)

    name = sa.Column(sa.String, nullable=False, unique=True)

    def __repr__(self):
        return f'<Department: {self.name}>'


class ProductCat(EntityMixin, db.Model):
    __tablename__ = 'product_categories'
    __upsert_index_elements__ = ('name',)

    name = sa.Column(sa.String, nullable=False, unique=True)

    def __repr__(self):
        return f'<ProductCat: {self.name}>'


class ProductBrand(EntityMixin, db.Model):
    __tablename__ = 'product_brands'
    __upsert_index_elements__ = ('name',)

    name = sa.Column(sa.String, nullable=False, unique=True)

    def __repr__(self):
        return f'<ProductBrand: {self.name}>'


class Product(EntityMixin, db.Model):
    __tablename__ = 'products'
    __upsert_index_elements__ = ('code',)

    department_id = sa.Column(sa.ForeignKey(Department.id, ondelete='restrict'), nullable=False)
    department = orm.relationship(Department, lazy='joined', innerjoin=True)
    category_id = sa.Column(sa.ForeignKey(ProductCat.id, ondelete='restrict'), nullable=False)
    category = orm.relationship(ProductCat, lazy='joined', innerjoin=True)
    brand_id = sa.Column(sa.ForeignKey(ProductBrand.id, ondelete='restrict'), nullable=True)
    brand = orm.relationship(ProductBrand, lazy='joined')

    code = sa.Column(sa.String, nullable=False, unique=True)
    per_case = sa.Column(sa.Integer)

    def __repr__(self):
        return f'<Product: {self.code}>'

    @classmethod
    def testing_create(cls, **kwargs):
        kwargs = tc_relation(cls, kwargs, 'department', Department)
        kwargs = tc_relation(cls, kwargs, 'category', ProductCat)
        return super().testing_create(**kwargs)

    @classmethod
    def delete_cascaded(cls):
        super().delete_cascaded()
        Department.delete_cascaded()
        ProductCat.delete_cascaded()


class Day(EntityMixin, db.Model):
    __tablename__ = 'days'
    __upsert_index_elements__ = ('date',)

    date = sa.Column(sa.Date, nullable=False, unique=True)

    def __repr__(self):
        return f'<Day: {self.date}>'

    @classmethod
    def testing_create(cls, **kwargs):
        # Note: this method doesn't use super().testing_create() due to the need for only one date
        # record for each date.
        kwargs.setdefault('date', dt.date.today())
        dbid = cls.upsert(**kwargs)
        return cls.query.get(dbid)


class ProductionDay(EntityMixin, db.Model):
    __tablename__ = 'production_days'
    __upsert_index_elements__ = ('day_id', 'product_id')
    __table_args__ = (
        # note: compound index
        sa.Index('uix_production_days', 'day_id', 'product_id', unique=True),
    )

    day_id = sa.Column(sa.ForeignKey(Day.id, ondelete='cascade'), nullable=False)
    # note: relationships can not be used implcitly.  See query_for() for examples of how to query.
    # The advantage is that it forces you to think about how you want the joins to work and doesn't
    # accidently create N+1 queries or pull more data from DB than you actually use.
    day = orm.relationship(Day, lazy='raise_on_sql')
    product_id = sa.Column(sa.ForeignKey(Product.id, ondelete='cascade'), nullable=False)
    product = orm.relationship(Product, lazy='raise_on_sql')

    ordered = sa.Column(sa.Numeric(6, 1), nullable=False, default=0, server_default='0')
    rolled_in = sa.Column(sa.Numeric(6, 1), nullable=False, default=0, server_default='0')
    add_on = sa.Column(sa.Numeric(6, 1), nullable=False, default=0, server_default='0')

    inventory = sa.Column(sa.Numeric(6, 1), nullable=False, default=0, server_default='0')
    priced_ahead = sa.Column(sa.Numeric(6, 1), nullable=False, default=0, server_default='0')
    rolled_out = sa.Column(sa.Numeric(6, 1), nullable=False, default=0, server_default='0')

    made_1 = sa.Column(sa.Numeric(6, 1), nullable=False, default=0, server_default='0')
    made_12 = sa.Column(sa.Numeric(6, 1), nullable=False, default=0, server_default='0')
    made_2 = sa.Column(sa.Numeric(6, 1), nullable=False, default=0, server_default='0')

    def __repr__(self):
        return f'<ProductionDay: {self.day.date}, {self.product.code}>'

    @classmethod
    def delete_cascaded(cls):
        super().delete_cascaded()
        Day.delete_cascaded()
        Product.delete_cascaded()

    @classmethod
    def testing_create(cls, **kwargs):
        kwargs = tc_relation(cls, kwargs, 'day', Day)
        kwargs = tc_relation(cls, kwargs, 'product', Product)
        return super().testing_create(**kwargs)

    @classmethod
    def by_date_prod(cls, date, prod_code):
        return cls.query_for(date=date, prod_code=prod_code).one_or_none()

    @classmethod
    def query_for(cls, *args, day_id=False, dept_id=None, prod_code=None, date=None, id=None):
        query = cls.query

        if id:
            query = query.filter_by(id=id)

        if dept_id or prod_code or 'product' in args:
            query = query.join(cls.product)

        if 'day' in args or date:
            query = query.join(cls.day)
            query = query.options(orm.contains_eager(cls.day))

        if 'product' in args:
            query = query.options(orm.contains_eager(cls.product))

        if day_id:
            query = query.filter(cls.day_id == day_id)

        if date:
            query = query.filter(Day.date == date)

        if prod_code:
            query = query.filter(Product.code == prod_code)

        if dept_id:
            query = query.filter(Product.department_id == dept_id)

        return query

    @hybrid_property
    def need_start(self):
        return self.ordered + self.rolled_in + self.add_on

    @hybrid_property
    def need_actual(self):
        return self.need_start - self.inventory - self.priced_ahead - self.rolled_out

    @hybrid_property
    def made_total(self):
        return self.made_1 + self.made_12 + self.made_2

    @hybrid_property
    def net_production(self):
        return self.made_total - self.need_actual
