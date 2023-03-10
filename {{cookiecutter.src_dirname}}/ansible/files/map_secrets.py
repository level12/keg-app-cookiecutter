"""
    This file exists so it can be used by the vars plugin as well as when developing locally.
"""

# What 1Password vault can I find my results in?  Any site whose FULLNAME field has this
# string will be available for processing (but not necessarily used).
onepass_vault = '{{ cookiecutter.onepass_secrets_vault }}'

# Map expected Ansible variable names to 1Password site usernames.  Details:
#   1) None as a value implies use the same value as the ansible variable name (just a shortcut)
#   2) The value of each item in this dict will be looked up against the 1Password site data using
#       fields: name, username, and id (in that order).  It must be complete match for the field.
#   3) There are three special suffixes that you can use on the key:
#       - _*: two variables will be created one for the username and one for the password.
#               e.g. 'app_api_*' --> app_api_username & app_api_password
#       - ~: the value returned will be the account username instead of the password.
#       - #: the note will be returned instead of the password
#
# You can list sites w/ their fields & values by running something like:
#   op item list --vault={{cookiecutter.onepass_secrets_vault}}
varmap = {
    # Variables that do not start with "app_" are expected to only be used in
    # the Python config file.  If they are used in Ansible directly, then they
    # should have the prefix.
    # Ansible Only:
    # -------------
    # App and Ansible
    # ---------------
    'app_db_pass_beta': 'db_pass_beta',
    'app_db_pass_prod': 'db_pass_prod',
    'app_flask_secret_key_beta': 'flask_secret_key_beta',
    'app_flask_secret_key_prod': 'flask_secret_key_prod',
    'app_rabbitmq_pass_beta': 'rabbitmq_pass_beta',
    'app_rabbitmq_pass_prod': 'rabbitmq_pass_prod',
    'pyapp3_sentry_dsn': 'sentry_dsn',
    # App config file only
    # --------------------
}
