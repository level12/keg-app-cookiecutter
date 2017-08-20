import logging

from keg_auth import AuthenticatedView, make_blueprint

log = logging.getLogger(__name__)

auth_bp = make_blueprint(__name__)


class ProtectedExample(AuthenticatedView):
    """ This is just an example of a view that will require being logged in to view it. """
    blueprint = auth_bp

    def get(self):
        return 'hi'
