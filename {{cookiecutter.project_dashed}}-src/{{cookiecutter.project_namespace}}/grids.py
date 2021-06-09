import flask
from keg_auth.grids import ActionColumn
import webgrid
from webgrid import filters

from .libs import grids as libgrids
from .model import entities as ents

# Filters

class DepartmentFilter(filters.OptionsIntFilterBase):
    options_from = lambda self: ents.Department.pairs('id', 'name')


class ProdBrandFilter(filters.OptionsIntFilterBase):
    options_from = lambda self: ents.ProductBrand.pairs('id', 'name')


class ProdCatFilter(filters.OptionsIntFilterBase):
    options_from = lambda self: ents.ProductCat.pairs('id', 'name')


# Columns

class DaysDate(webgrid.LinkColumnBase):
    def create_url(self, record):
        return flask.url_for('private.production-day:summary', day_id=record.id)

    def extract_and_format_data(self, record):
        return record.date


# Grids

class Days(libgrids.Grid):
    webgrid.Column('Id', ents.Day.id, visible=False)
    DaysDate('Date', ents.Day.date, filters.DateFilter)


class Department(libgrids.Grid):
    ActionColumn(
        'Actions', ents.Department.id,
        edit_endpoint='private.department:edit',
        delete_endpoint='private.department:delete',
    )
    webgrid.Column('Name', ents.Department.name, filters.TextFilter)

    def query_prep(self, query, has_sort, has_filters):
        if not has_sort:
            query = query.order_by('name')

        return query

class ProductBrand(libgrids.Grid):
    ActionColumn(
        'Actions', ents.ProductBrand.id,
        edit_endpoint='private.product-brand:edit',
        delete_endpoint='private.product-brand:delete',
    )
    webgrid.Column('Name', ents.ProductBrand.name, filters.TextFilter)

    def query_prep(self, query, has_sort, has_filters):
        if not has_sort:
            query = query.order_by('name')

        return query


class ProductCat(libgrids.Grid):
    ActionColumn(
        'Actions', ents.ProductCat.id,
        edit_endpoint='private.product-cat:edit',
        delete_endpoint='private.product-cat:delete',
    )
    webgrid.Column('Name', ents.ProductCat.name, filters.TextFilter)

    def query_prep(self, query, has_sort, has_filters):
        if not has_sort:
            query = query.order_by('name')

        return query


class Product(libgrids.Grid):
    ActionColumn(
        'Actions', ents.Product.id,
        edit_endpoint='private.product:edit',
        delete_endpoint='private.product:delete',
    )
    webgrid.Column('Code', ents.Product.code, filters.TextFilter)
    webgrid.Column('Per Case', ents.Product.per_case, filters.IntFilter)
    webgrid.Column('Category', ents.ProductCat.name.label('pc_name'),
        ProdCatFilter(ents.ProductCat.id))
    webgrid.Column('Department', ents.Department.name.label('dep_name'),
        DepartmentFilter(ents.Department.id))
    webgrid.Column('Brand', ents.ProductBrand.name.label('brand_name'),
        ProdBrandFilter(ents.ProductBrand.id))

    def query_prep(self, query, has_sort, has_filters):
        query = query.select_from(
            ents.Product
        ).join(
            ents.Product.category
        ).join(
            ents.Product.department
        ).join(
            ents.Product.brand
        )

        if not has_sort:
            query = query.order_by('code')

        return query
