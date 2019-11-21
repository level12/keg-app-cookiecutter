from keg_auth.forms import user_form as user_form_base


def user_form(config, allow_superuser, endpoint, fields=['name', 'is_enabled']):
    return user_form_base(config, allow_superuser, endpoint, fields=fields)
