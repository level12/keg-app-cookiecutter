import itertools

import sqlalchemy as sa
from sqlalchemy.sql import select

from ..model import entities as ents


pd_tbl = ents.ProductionDay.__table__
prod_cat_tbl = ents.ProductCat.__table__
dept_tbl = ents.Department.__table__
prod_tbl = ents.Product.__table__


def dept_totals(day_id):
    cat_q = select([
        ents.Product.department_id.label('dept_id'),
        ents.ProductCat.name.label('category_name'),
        sa.func.sum(ents.ProductionDay.made_1).label('shift_1'),
        sa.func.sum(ents.ProductionDay.made_2).label('shift_2'),
        sa.func.sum(ents.ProductionDay.need_actual).label('need'),
        sa.func.sum(ents.ProductionDay.net_production).label('net'),
    ]).select_from(
        pd_tbl.join(prod_tbl).join(prod_cat_tbl)
    ) \
        .where(ents.ProductionDay.day_id == day_id) \
        .group_by(ents.Product.department_id, ents.ProductCat.name) \
        .order_by(ents.Product.department_id, ents.ProductCat.name)

    results = ents.db.engine.execute(cat_q).fetchall()

    dept_recs = {
        dept_id: list(dept_recs)
        for dept_id, dept_recs in itertools.groupby(results, lambda rec: rec.dept_id)
    }

    dept_totals = {}
    for dept_id, recs in dept_recs.items():
        totals = {'shift_1': 0, 'shift_2': 0, 'need': 0, 'net': 0}
        for rec in recs:
            totals['shift_1'] += rec.shift_1
            totals['shift_2'] += rec.shift_2
            totals['need'] += rec.need
            totals['net'] += rec.net
        dept_totals[dept_id] = totals

    return dept_recs, dept_totals
