from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_current_user, verify_jwt_in_request, get_jwt
from app.extensions import logger, jwt
from app.models.token_blocked import TokenBlocked
from app.models.user import User
from app.blueprints.auth import user_service, token_blocklist_service

@jwt.user_identity_loader
def user_identity_lookup(user: User):
    return user.get_id()

@jwt.user_lookup_loader
def user_loader_callback(_jwt_header, jwt_data):
    logger.info(f'{jwt_data=}{_jwt_header=}')
    user_id = jwt_data['sub']
    user = user_service.get_user_by_id(user_id)
    if not user:
        return None
    
    return user

@jwt.token_in_blocklist_loader
def check_if_token_revoked(_jwt_header, jwt_data: dict) -> bool:
    jti = jwt_data["jti"]

    is_revoked = token_blocklist_service.is_token_in_blocklist(TokenBlocked(jti=jti))
    
    return is_revoked

def jwt_user_required():
    '''Decorator to require that a user is an admin to access a route.'''
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            current_user = get_current_user()
            if current_user:
                return fn(*args, **kwargs)
            else:
                logger.error('Unauthorized request: User not found.')
                return jsonify(msg="Unauthorized request: User not found."), 404

        return decorator

    return wrapper

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
                return jsonify(msg="Unauthorized request: Must be Admin"), 401

        return decorator

    return wrapper