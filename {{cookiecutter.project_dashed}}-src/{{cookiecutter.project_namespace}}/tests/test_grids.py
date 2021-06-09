from .. import grids
from ..libs import testing
from ..model import entities as ents


class TestDepartmentGrid:
    @classmethod
    def setup_class(cls):
        ents.Department.delete_cascaded()

    @testing.inrequest('/')
    def test_it(self):
        ents.Department.testing_create(name='Whole Birds')
        ga = testing.GridAssertions(grids.Department())

        ga.assert_grid_matches([
            ['Actions', 'Name'],
            ['', 'Whole Birds'],
        ])


class TestProductCatGrid:
    @classmethod
    def setup_class(cls):
        ents.ProductCat.delete_cascaded()

    @testing.inrequest('/')
    def test_it(self):
        ents.ProductCat.testing_create(name='Bagged')
        ga = testing.GridAssertions(grids.ProductCat())

        ga.assert_grid_matches([
            ['Actions', 'Name'],
            ['', 'Bagged'],
        ])


class TestProductBrandGrid:
    @classmethod
    def setup_class(cls):
        ents.ProductBrand.delete_cascaded()

    @testing.inrequest('/')
    def test_it(self):
        ents.ProductBrand.testing_create(name='Whole Foods')
        ga = testing.GridAssertions(grids.ProductBrand())

        ga.assert_grid_matches([
            ['Actions', 'Name'],
            ['', 'Whole Foods'],
        ])


class TestProductGrid:
    @classmethod
    def setup_class(cls):
        ents.Product.delete_cascaded()

    @testing.inrequest('/')
    def test_it(self):
        brand = ents.ProductBrand.testing_create(name='Hot Iron')
        ents.Product.testing_create(code='abc', per_case=5, category__name='foo',
            department__name='bar', brand=brand)
        ga = testing.GridAssertions(grids.Product())

        ga.assert_grid_matches([
            ['Actions', 'Code', 'Per Case', 'Category', 'Department', 'Brand'],
            ['', 'abc', '5', 'foo', 'bar', 'Hot Iron'],
        ])
