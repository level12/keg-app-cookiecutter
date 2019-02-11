from keg_auth.forms import user_form as user_form_base
from keg_elements.forms import ModelForm

from {{cookiecutter.project_namespace}}.model import entities


class Blog(ModelForm):
    class Meta:
        model = entities.Blog
        only = ['title', 'posted_utc']


def user_form(config, allow_superuser, endpoint, fields=['name', 'is_enabled']):
    return  user_form_base(config, allow_superuser, endpoint, fields=fields)
