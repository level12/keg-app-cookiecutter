from .auth import auth_bp
from .public import public_bp
from .private import private_bp

blueprints = (auth_bp, public_bp, private_bp)
