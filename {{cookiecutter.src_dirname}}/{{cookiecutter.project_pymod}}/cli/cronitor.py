import flask

from ..app import {{cookiecutter.project_class}}


class InvalidCronitorConfig(Exception):
    pass


@{{cookiecutter.project_class}}.cli.group(name="cronitor")
def _cronitor():
    """Cronitor tasks"""


@_cronitor.command()
def apply_config():
    """Validate cronitor config"""
    cronitor = flask.current_app.cronitor
    cronitor.read_config('./cronitor.yaml')
    was_update_successful = cronitor.apply_config()
    if not was_update_successful:
        raise InvalidCronitorConfig()

