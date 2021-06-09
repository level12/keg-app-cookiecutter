from blazeutils import strings
import flask
from keg.web import route
from keg_auth import requires_user, requires_permissions
from keg_auth.views import CrudView

from .. import forms, grids
from ..model import entities as ents, queries
from ..libs.views import BaseView, GridView


@requires_user()
class ProtectedBlueprint(flask.Blueprint):
    pass


private_bp = ProtectedBlueprint('private', __name__,)


# Note: no permission required, just authentication
class Days(GridView):
    blueprint = private_bp
    grid_cls = grids.Days
    title = 'Production Days'


@requires_permissions('manager')
class Department(CrudView):
    blueprint = private_bp
    url = '/departments'
    object_name = 'Department'
    object_name_plural = 'Departments'
    form_cls = forms.Department
    grid_cls = grids.Department
    orm_cls = ents.Department


@requires_permissions('manager')
class ProductBrand(CrudView):
    blueprint = private_bp
    url = '/product-brands'
    object_name = 'Product Brand'
    object_name_plural = 'Product Brands'
    form_cls = forms.ProductBrand
    grid_cls = grids.ProductBrand
    orm_cls = ents.ProductBrand


@requires_permissions('manager')
class ProductCat(CrudView):
    blueprint = private_bp
    url = '/product-categories'
    object_name = 'Product Category'
    object_name_plural = 'Product Categories'
    form_cls = forms.ProductCat
    grid_cls = grids.ProductCat
    orm_cls = ents.ProductCat


@requires_permissions('manager')
class Product(CrudView):
    blueprint = private_bp
    url = '/products'
    object_name = 'Product'
    object_name_plural = 'Products'
    form_cls = forms.Product
    grid_cls = grids.Product
    orm_cls = ents.Product


class ProductionDay(BaseView):
    blueprint = private_bp

    def prep(self, day_id, tab_name):
        depts = ents.Department.query.order_by('name').all()
        self.assign('day_id', day_id)
        self.assign('day_ent', ents.Day.query.get(day_id))
        self.assign(f'tab_active_{tab_name}', 'active')
        self.assign('tab_name', tab_name)
        self.assign('departments', depts)
        return depts

    @route('/production-day/<int:day_id>')
    def summary(self, day_id):
        depts = self.prep(day_id, 'summary')
        dept_map = {d.name: d for d in depts}

        dept_groups, dept_totals = queries.dept_totals(day_id)
        self.assign('dept_groups', dept_groups)
        self.assign('dept_totals', dept_totals)
        self.assign('dept_map', dept_map)

    @route('/production-day/<int:day_id>/dept/<int:dept_id>')
    def dept(self, day_id, dept_id):
        records = ents.ProductionDay.query_for('product', day_id=day_id, dept_id=dept_id)

        if flask.request.args.get('json') is not None:
            def extract_json(rec):
                return {
                    'id': rec.id,
                    'code': rec.product.code,
                    'ordered': rec.ordered,
                    'rolledIn': rec.rolled_in,
                    'addOn': rec.add_on,
                    'inventory': rec.inventory,
                    'pricedAhead': rec.priced_ahead,
                    'rolledOut': rec.rolled_out,
                    'made1': rec.made_1,
                    'made12': rec.made_12,
                    'made2': rec.made_2,
                    'prodCatId': rec.product.category_id,
                }
            records = [extract_json(rec) for rec in records]
            cat_ids = {rec['prodCatId'] for rec in records}
            prod_cats = ents.ProductCat.query.filter(ents.ProductCat.id.in_(cat_ids))
            return flask.jsonify(
                records=records,
                cats=[{'id': cat.id, 'name': cat.name} for cat in prod_cats]
            )

        self.prep(day_id, 'dept')
        self.assign('dept_id', dept_id)
        self.assign('records', records)


class ProductionDayUpdateField(BaseView):
    blueprint = private_bp
    field_names = ('ordered', 'add_on', 'rolled_in', 'inventory', 'priced_ahead', 'rolled_out',
        'made_1', 'made_12', 'made_2')

    def post(self):
        req_data = flask.request.get_json()
        pd_id = req_data['id']
        field_name = req_data['fieldName']
        value = req_data['value']

        pd = ents.ProductionDay.query.get(pd_id)
        if pd is None:
            return 'no record', 200

        field_name = strings.case_mc2us(field_name)
        if 'made' in field_name:
            field_name = field_name.replace('made', 'made_')

        assert field_name in self.field_names, field_name

        setattr(pd, field_name, value)
        ents.db.session.commit()

        return '1', 200
