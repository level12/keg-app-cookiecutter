
import logging
import keg_auth

log = logging.getLogger(__name__)


class AuthManager(keg_auth.AuthManager):
    def create_user_cli(self, email, extra_args):
        return self.create_user({
            'email': email,
            'name': extra_args[0] if extra_args else ''
        })
