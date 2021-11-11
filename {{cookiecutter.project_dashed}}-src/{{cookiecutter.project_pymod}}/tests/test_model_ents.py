from keg_elements.testing import (
    ColumnCheck,
    EntityBase,
)
import pytest
import sqlalchemy.exc

from ..model import entities as ents


class TestUser(EntityBase):
    entity_cls = ents.User
    column_checks = [
        ColumnCheck('is_verified'),
        ColumnCheck('is_enabled'),
        ColumnCheck('is_superuser'),
        ColumnCheck('session_key', unique=True),
        ColumnCheck('email', unique=True),
        ColumnCheck('password', required=False),
        ColumnCheck('name'),
        ColumnCheck('settings', required=False),
        ColumnCheck('last_login_utc', required=False),
        ColumnCheck('disabled_utc', required=False)
    ]


class TestProduct:
    @classmethod
    def setup_class(cls):
        ents.Product.delete_cascaded()

    def test_unique(self):
        department = ents.Department.testing_create()
        category = ents.ProductCat.testing_create()

        assert ents.Product.query.count() == 0

        ents.Product.upsert(code='0123', per_case=1, department_id=department.id,
            category_id=category.id)
        ents.Product.upsert(code='0123', per_case=2, department_id=department.id,
            category_id=category.id)

        ents.db.session.commit()

        prod = ents.Product.query.one()
        assert prod.per_case == 2
        assert prod.code == '0123'
        assert prod.department is department
        assert prod.category is category


class TestProductionDay:

    def setup(self):
        ents.ProductionDay.delete_cascaded()

    def test_hybrid_props(self):
        ents.ProductionDay.testing_create(
            ordered=1,
            rolled_in=2,
            add_on=3,
            inventory=4,
            priced_ahead=5,
            rolled_out=6,
            made_1=7,
            made_12=8,
            made_2=9,
        )
        ents.db.session.commit()

        pd = ents.ProductionDay.query.one()
        assert pd.need_start == 6
        assert pd.need_actual == -9
        assert pd.made_total == 24
        assert pd.net_production == 33

        pd = ents.ProductionDay.testing_create(ordered=20, made_1=10)
        assert pd.net_production == -10

        pd = ents.ProductionDay.testing_create(ordered=10, made_1=20)
        assert pd.net_production == 10

    def test_query_for(self):
        day = ents.Day.testing_create(date='2020-05-20')
        day2 = ents.Day.testing_create(date='2020-05-21')
        prod = ents.Product.testing_create()
        prod2 = ents.Product.testing_create()
        ents.ProductionDay.testing_create(day=day, product=prod)
        ents.ProductionDay.testing_create(day=day, product=prod2)
        ents.ProductionDay.testing_create(day=day2, product=prod)

        day_id = day.id
        dept_id = prod.department_id
        prod_code = prod.code
        ents.db.session.remove()

        pd = ents.ProductionDay.query_for(day_id=day_id, dept_id=dept_id).one()
        with pytest.raises(sqlalchemy.exc.InvalidRequestError):
            assert pd.day.date

        pd = ents.ProductionDay.query_for('day', day_id=day_id, dept_id=dept_id).one()
        assert pd.day.date.isoformat() == '2020-05-20'

        pd = ents.ProductionDay.query_for(day_id=day_id, prod_code=prod_code).one()
        with pytest.raises(sqlalchemy.exc.InvalidRequestError):
            assert pd.product

        pd = ents.ProductionDay.query_for('product', day_id=day_id, prod_code=prod_code).one()
        assert pd.product

    def test_by_data_prod(self):
        pd = ents.ProductionDay.testing_create(day__date='2020-08-05', product__code='abc')
        assert ents.ProductionDay.by_date_prod('2020-08-05', 'abc') is pd
