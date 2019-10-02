from keg_auth.grids import ActionColumn
import webgrid
import webgrid.flask

from {{cookiecutter.project_namespace}}.model import entities
from {{cookiecutter.project_namespace}}.libs.grids import Grid


class Blog(Grid):
    ActionColumn(
        '',
        entities.Blog.id,
        edit_endpoint='private.blog:edit',
        delete_endpoint='private.blog:delete',
    )
    webgrid.Column('Title', entities.Blog.title, webgrid.filters.TextFilter)
