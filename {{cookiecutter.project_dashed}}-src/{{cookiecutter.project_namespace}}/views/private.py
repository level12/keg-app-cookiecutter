import logging

import flask
from keg.web import BaseView
from keg_auth import (
    CrudView,
    requires_permissions,
    requires_user,
)

from {{cookiecutter.project_namespace}} import (
    forms,
    grids,
)
from {{cookiecutter.project_namespace}}.model import entities as ents

log = logging.getLogger(__name__)

# Attach protected views to a separate blueprint
#   Note: if all requirements are the same, the blueprint can be decorated
#   directly.
private_bp = flask.Blueprint('private', __name__,)


# Decorating the view method drives authentication requirement. Methods,
#   classes, and blueprints may be decorated in the same way, with the same
#   result. Also drives what navigation links are available.
@private_bp.route('/protected-example')
@requires_user
def protected_example():
    return 'hi'


# Permissions are set up on app initialization
# See Keg Auth readme for requires_permission examples
#  - https://github.com/level12/keg-auth
@requires_permissions('app-permission')
class PermissionExample(BaseView):
    blueprint = private_bp

    def get(self):
        return 'permission-example'


@requires_user
class Blog(CrudView):
    blueprint = private_bp
    url = '/blog-posts'
    object_name = 'Blog Post'
    orm_cls = ents.Blog
    grid_cls = grids.Blog
    form_cls = forms.Blog
