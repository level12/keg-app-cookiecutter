import logging

import flask

log = logging.getLogger(__name__)

# Attach protected views to a separate blueprint
#   Note: if all requirements are the same, the blueprint can be decorated
#   directly.
private_bp = flask.Blueprint('private', __name__,)
