from keg_elements.forms import FieldMeta, ModelForm, SelectField
from keg_elements.forms.validators import ValidateUnique
from wtforms.fields import IntegerField, StringField
from wtforms.validators import input_required, optional

from .model import entities as ents


class Department(ModelForm):
    class Meta:
        model = ents.Department


class ProductCat(ModelForm):
    class Meta:
        model = ents.ProductCat


class ProductBrand(ModelForm):
    class Meta:
        model = ents.ProductBrand


class Product(ModelForm):
    class Meta:
        model = ents.Product

    department_id = SelectField('Department', validators=[input_required()])
    category_id = SelectField('Category', validators=[input_required()])
    brand_id = SelectField('Brand', validators=[optional()])
    code = StringField('Code', validators=[input_required(), ValidateUnique()])
    per_case = IntegerField('Per Case', validators=[optional()])

    class FieldsMeta:
        code = FieldMeta(extra_validators=[ValidateUnique()])

    def after_init(self, args, kwargs):
        self.department_id.choices = ents.Department.pairs(
            'id', 'name', order_by=(ents.Department.name,)
        )
        self.category_id.choices = ents.ProductCat.pairs(
            'id', 'name', order_by=(ents.ProductCat.name,)
        )
        self.brand_id.choices = ents.ProductBrand.pairs(
            'id', 'name', order_by=(ents.ProductBrand.name,)
        )

    def get_object_by_field(self, field):
        return ents.Product.get_by(code=field.data)

    @property
    def obj(self):
        return self._obj
