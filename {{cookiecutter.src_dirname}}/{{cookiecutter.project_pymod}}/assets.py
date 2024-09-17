from webassets import Bundle

from flask_assets import Environment


environment = Environment()

app_css = Bundle(
    'css/scss/app.scss',
    filters='libsass',
    output='css/app.css',
    depends=['css/scss/*.scss'],
)

environment.register('app_css', app_css)
