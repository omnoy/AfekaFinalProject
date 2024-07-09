from flask import Response, request, jsonify
from flask_jwt_extended import get_current_user, create_access_token, get_jwt
from pydantic import ValidationError
from app.blueprints.auth import bp, token_blocklist_service, user_service
from app.blueprints.jwt_user_verification import jwt_user_required
from app.models.user import User
from app.extensions import logger
from app.models.token_blocked import TokenBlocked
from app.models.exceptions.object_already_exists_exception import ObjectAlreadyExistsException

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

        if "role" in user_data.keys() and user_data['role'] == "admin_user":
            logger.error('Unauthorized role, cannot register as admin')
            return jsonify(error="Unauthorized role, cannot register as admin"), 403

        user = User(**user_data)
        user = user_service.create_user(user)
        claims = {"is_admin": user.is_admin()}
        access_token = create_access_token(identity=user, additional_claims=claims)

        return jsonify(access_token=access_token, 
                       user=user.model_dump(exclude='password')), 200
    
    except ObjectAlreadyExistsException as e:
        logger.exception(e)
        return jsonify(error=str(e)), 409
    except ValidationError as e:
        logger.exception(e)
        return jsonify(error=f"Invalid JSON input: {str(e)}"), 400
    except Exception as e:
        logger.exception(e)
        return jsonify(error=str(e)), 500
    

@bp.route('/login', methods=['POST'])
def login():
    logger.info('Logging in user')
    try:
        login_data = request.get_json()
        logger.info(f'{login_data=}')
        if login_data is None:
            logger.exception('No JSON input for login')
            return jsonify(error="No JSON input"), 400

        user = user_service.get_user_by_email(login_data['email'])
        if user:
            if user.check_password(login_data['password']):
                claims = {"is_admin": user.is_admin()}
                access_token = create_access_token(identity=user, additional_claims=claims)
            else:
                logger.error(f'Invalid Password for {login_data}')
                return jsonify(error="Invalid Password"), 401

            return jsonify(access_token=access_token, 
                           user=user.model_dump(exclude='password')), 200
        else:
            logger.error(f'Invalid Email for {login_data}')
            return jsonify(error="Invalid Email"), 401
    except Exception as e:
        logger.exception(e)
        return jsonify(error=str(e)), 500
        
@bp.route('/logout', methods=['POST'])
@jwt_user_required()
def logout():
    logger.info('Logging out user')
    try:
        current_user = get_current_user()
        
        jti = get_jwt()["jti"]

        token_blocklist_service.add_token_to_blocklist(TokenBlocked(jti=jti))

        logger.info(f"User {current_user} logged out.")
        return Response(status=200)
    
    except Exception as e:
        logger.exception(e)
        return jsonify(error=str(e)), 500