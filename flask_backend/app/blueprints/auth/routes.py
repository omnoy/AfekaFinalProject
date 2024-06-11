from flask import request, make_response, jsonify, flash, abort
from flask_jwt_extended import get_current_user, create_access_token, create_refresh_token, jwt_required, get_jwt
from pydantic import ValidationError
from pydantic.json import pydantic_encoder
from app.blueprints.auth import bp, user_service
from app.models.user import User
from app.extensions import logger, jwt
from app.logic.mongo.database import get_token_blocklist
from app.models.token_blocked import TokenBlocked
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
    try:
        user_data = request.get_json(silent=True)
        if user_data is None:
            logger.error('No JSON input for registration')
            abort(400, "No JSON input")
        
        user = User(**user_data)
        user = user_service.create_user(user)

        access_token = create_access_token(identity=user)

        return jsonify({
                "message": "User Registered successfully",
                "access_token": access_token,
                "user": user.model_dump_json(by_alias=True, exclude='password')
            }), 200
    
    except ValidationError as e:
        logger.exception(e)
        abort(400,  f"Invalid JSON input: {str(e)}")
    except Exception as e:
        logger.exception(e)
        abort(500, str(e))
    
    

@bp.route('/login', methods=['GET', 'POST'])
def login():
    try:
        login_data = request.get_json()
        if login_data is None:
                logger.exception('No JSON input for login')
                return abort(400, "No JSON input")

        user = user_service.get_user_by_email(login_data['email'])
        if user and user.check_password(login_data['password']):
            access_token = create_access_token(identity=user)
            refresh_token = create_refresh_token(identity=user)

            return jsonify({
                    "message": "User Logged In successfully",
                    "tokens": {
                            "access": access_token, 
                            "refresh": refresh_token
                    },
                    "user": user.model_dump_json(by_alias=True, exclude="password", indent=4)
                }), 200
        else:
            logger.error(f'Invalid Username or Password for {login_data}')
            return jsonify("Invalid Username or Password"), 401
    except Exception as e:
        logger.exception(e)
        abort(500, str(e))
        
@bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    current_user = get_current_user()
    jti = get_jwt()["jti"]

    get_token_blocklist().insert_one(TokenBlocked(jti=jti).__dict__)

    logger.info(f"User {current_user} logged out.")
    return jsonify({"message":f"User {current_user.username} logout successful"}), 200 