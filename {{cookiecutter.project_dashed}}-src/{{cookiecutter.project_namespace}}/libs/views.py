from blazeutils import strings
import flask
from keg.web import BaseView as _BaseView, ImmediateResponse


class BaseView(_BaseView):
    def calc_class_fname(self):
        return strings.case_cw2dash(self.__class__.__name__)
