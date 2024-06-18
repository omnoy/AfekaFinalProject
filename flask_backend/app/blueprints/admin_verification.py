from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from app.extensions import logger

def jwt_admin_required():
    '''Decorator to require that a user is an admin to access a route.'''
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["is_admin"]:
                return fn(*args, **kwargs)
            else:
                logger.error('Unauthorized request: Must be Admin')
                return jsonify(msg="Unauthorized request: Must be Admin"), 403

        return decorator

    return wrapper