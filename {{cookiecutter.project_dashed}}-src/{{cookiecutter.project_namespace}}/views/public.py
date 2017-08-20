import logging

import flask
from keg.web import BaseView, rule

public_bp = flask.Blueprint('public', __name__,)
log = logging.getLogger(__name__)


@public_bp.route('/')
def home():
    return 'Hello World from {{cookiecutter.project_name}}!'


class Hello(BaseView):
    blueprint = public_bp
    rule('<name>')

    def get(self, name='World'):
        self.assign('name', name)
