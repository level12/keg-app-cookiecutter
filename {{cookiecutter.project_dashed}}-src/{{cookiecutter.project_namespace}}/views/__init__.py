from .auth import auth_bp
from .private import private_bp
from .public import public_bp

blueprints = (public_bp, private_bp, auth_bp)
