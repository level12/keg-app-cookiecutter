import logging

from keg_auth import make_blueprint
from keg_auth.views import User as UserBase

from {{cookiecutter.project_namespace}} import forms

log = logging.getLogger(__name__)


class User(UserBase):
    # need to make this a static method so it isn't bound on the view instance
    form_cls = staticmethod(forms.user_form)


# This blueprint is for keg-auth's views (Login, user management, etc.)
auth_bp = make_blueprint(__name__, user_crud_cls=User)
