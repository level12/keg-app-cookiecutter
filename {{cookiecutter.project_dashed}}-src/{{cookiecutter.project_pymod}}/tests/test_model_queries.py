from ..model import entities as ents, queries


class TestQueries:
    def setup(self):
        ents.ProductionDay.delete_cascaded()

    def test_debt_totals(self):
        day = ents.Day.testing_create(date='2020-08-16')
        day2 = ents.Day.testing_create(date='2020-08-15')
        wb_dept = ents.Department.testing_create(name='Whole Birds')
        foo_dept = ents.Department.testing_create(name='Foo')
        tied = ents.ProductCat.testing_create(name='Tied')
        packed = ents.ProductCat.testing_create(name='Packed')

        # packed today
        ents.ProductionDay.testing_create(product__department=wb_dept, product__category=packed,
            day=day, made_1=2, made_12=3, made_2=4)
        ents.ProductionDay.testing_create(product__department=wb_dept, product__category=packed,
            day=day, made_1=11, made_12=2, made_2=3)

        # tied today
        ents.ProductionDay.testing_create(product__department=wb_dept, product__category=tied,
            day=day, made_1=1, made_12=2, made_2=3)
        ents.ProductionDay.testing_create(product__department=wb_dept, product__category=tied,
            day=day, made_1=11, made_12=2, made_2=3)

        # different dept
        ents.ProductionDay.testing_create(product__department=foo_dept, product__category=tied,
            day=day, made_1=11, made_12=2, made_2=3)

        # tied yesterday, should impact numbers
        ents.ProductionDay.testing_create(product__department=wb_dept, product__category=tied,
            day=day2, made_1=10, made_12=20, made_2=30)

        dept_groups, dept_totals = queries.dept_totals(day.id)

        assert len(dept_groups) == 2

        wb_recs = dept_groups[wb_dept.id]
        assert len(wb_recs) == 2

        foo_recs = dept_groups[foo_dept.id]
        assert len(foo_recs) == 1

        rec = wb_recs[0]
        assert rec.category_name == 'Packed'
        assert rec.shift_1 == 13
        assert rec.shift_2 == 7
        assert rec.need == 0
        assert rec.net == 25

        rec = wb_recs[1]
        assert rec.category_name == 'Tied'
        assert rec.shift_1 == 12
        assert rec.shift_2 == 6

        rec = foo_recs[0]
        assert rec.category_name == 'Tied'
        assert rec.shift_1 == 11
        assert rec.shift_2 == 3

        wb_totals = dept_totals[wb_dept.id]
        assert wb_totals['shift_1'] == 25
        assert wb_totals['shift_2'] == 13
        assert wb_totals['need'] == 0
        assert wb_totals['net'] == 47

        foo_totals = dept_totals[foo_dept.id]
        assert foo_totals['shift_1'] == 11
        assert foo_totals['shift_2'] == 3
        assert foo_totals['need'] == 0
        assert foo_totals['net'] == 16
