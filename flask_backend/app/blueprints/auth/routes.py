from flask import request, jsonify, abort
from flask_jwt_extended import get_current_user, create_access_token, jwt_required, get_jwt
from pydantic import ValidationError
from app.blueprints.auth import bp, user_service
from app.models.user import User
from app.extensions import logger, jwt
from app.logic.mongo.database import get_token_blocklist
from app.models.token_blocked import TokenBlocked
from app.models.exceptions.object_already_exists_exception import ObjectAlreadyExistsException
from app.models.user_role import UserRole
# basic commands

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
    token = get_token_blocklist().find_one({"jti": jti})

    return token is not None

@bp.route('/register', methods=['POST'])
def register():
    logger.info('Registering user')
    try:
        user_data = request.get_json(silent=True)
        logger.info(f'{user_data=}')
        if user_data is None:
            logger.error('No JSON input for registration')
            return jsonify(error="No JSON input"), 400

        if "id" in user_data.keys():
            logger.error('Cannot set ID for user registration')
            return jsonify(error="Cannot set ID for user registration"), 400

        if "role" in user_data.keys() and user_data['role'] == 'admin':
            logger.error('Unauthorized role, cannot register as admin')
            return jsonify(error="Unauthorized role, cannot register as admin"), 403

        user = User(**user_data)
        user = user_service.create_user(user)
        claims = {"is_admin": user.is_admin()}
        access_token = create_access_token(identity=user, additional_claims=claims)

        return jsonify(msg="User Registered successfully", 
                       access_token=access_token, 
                       user=user.model_dump(exclude='password')), 200
    
    except ObjectAlreadyExistsException as e:
        logger.exception(e)
        abort(409, str(e))
    except ValidationError as e:
        logger.exception(e)
        abort(400,  f"Invalid JSON input: {str(e)}")
    except Exception as e:
        logger.exception(e)
        abort(500, str(e))
    

@bp.route('/login', methods=['GET', 'POST'])
def login():
    logger.info('Logging in user')
    try:
        login_data = request.get_json()
        logger.info(f'{login_data=}')
        if login_data is None:
            logger.exception('No JSON input for login')
            return jsonify(error="No JSON input"), 400

        user = user_service.get_user_by_email(login_data['email'])
        if user and user.check_password(login_data['password']):
            claims = {"is_admin": user.is_admin()}
            access_token = create_access_token(identity=user, additional_claims=claims)

            return jsonify(msg="User Logged In successfully", 
                           access_token=access_token, 
                           user=user.model_dump(exclude='password')), 200
        else:
            logger.error(f'Invalid Username or Password for {login_data}')
            return jsonify(error="Invalid Username or Password"), 401
    except Exception as e:
        logger.exception(e)
        abort(500, str(e))
        
@bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    logger.info('Logging out user')
    try:
        current_user = get_current_user()
        if current_user is None:
            logger.error('No user found')
            return jsonify(error="No user found"), 400
        
        jti = get_jwt()["jti"]

        get_token_blocklist().insert_one(TokenBlocked(jti=jti).__dict__)

        logger.info(f"User {current_user} logged out.")
        return jsonify(msg=f"User {current_user.username} logout successful"), 200 
    
    except Exception as e:
        logger.exception(e)
        abort(500, str(e))