from keg_auth.grids import ActionColumn
import webgrid
import webgrid.flask

from {{cookiecutter.project_namespace}}.model import entities


class Grid(webgrid.BaseGrid):
    manager = webgrid.flask.WebGrid()
    session_on = True


class Blog(Grid):
    ActionColumn(
        '',
        entities.Blog.id,
        edit_endpoint='private.blog:edit',
        delete_endpoint='private.blog:delete',
    )
    webgrid.Column('Title', entities.Blog.title, webgrid.filters.TextFilter)
