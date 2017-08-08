from keg import Keg

from {{cookiecutter.project_namespace}}.views import public


class {{cookiecutter.project_class}}(Keg):
    import_name = '{{cookiecutter.project_namespace}}'
    use_blueprints = [public]
