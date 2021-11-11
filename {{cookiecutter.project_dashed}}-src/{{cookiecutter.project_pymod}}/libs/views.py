from blazeutils import strings
import flask
from keg.web import BaseView as _BaseView, ImmediateResponse


class BaseView(_BaseView):
    def calc_class_fname(self):
        return strings.case_cw2dash(self.__class__.__name__)


class DependencyError(Exception):
    pass


class GridView(BaseView):
    grid_cls = None
    template = 'includes/grid-view.html'
    title = None

    def get(self):
        return self.render_grid()

    def render_grid(self):
        if self.grid_cls is None:
            raise NotImplementedError(
                'You must set {}.grid_cls to render a grid'.format(self.__class__.__name__)
            )

        g = self.grid_cls()
        g.apply_qs_args()

        if hasattr(self, 'setup_grid'):
            self.setup_grid(g)

        if g.export_to == 'xls':
            if g.xls is None:
                raise DependencyError('The xlwt library has to be installed for Excel export.')
            raise ImmediateResponse(g.xls.as_response())

        template_args = {
            'grid': g,
            'title': self.title,
        }

        return flask.render_template(self.template, **template_args)
