from bson import json_util
from flask import request, render_template, jsonify, flash, abort
from pydantic.json import pydantic_encoder
from pydantic import TypeAdapter, ValidationError
from app.blueprints.users import bp, user_service
from app.models.user import User
from app.models.user_role import UserRole
from flask_jwt_extended import jwt_required, get_current_user
from app.extensions import logger
from app.blueprints.admin_verification import jwt_admin_required

@bp.route('/update', methods=['PUT'])
@jwt_required()
def update_user():
    logger.info('Updating user')
    try:
        user = get_current_user()
        if user is None:
            logger.error('No user found')
            return jsonify(msg="No user found"), 404
        
        user_data = request.get_json(silent=True)
        logger.info(f'{user_data=}')
        if user_data is None:
            logger.error('No JSON input for user update')
            return jsonify(error="No JSON input for user update"), 400
        
        for invalid_key in ['id', 'email', 'role']:
            if invalid_key in user_data.keys() and user_data[invalid_key] != getattr(user, invalid_key):
                logger.error(f'Cannot set {invalid_key} for user update')
                return jsonify(error=f"Cannot set {invalid_key} for user update"), 400
        
        user = user_service.update_user(user.get_id(), User(**user_data))
        
        return jsonify(msg="User updated successfully", user=user.model_dump()), 200
         
    except ValidationError as e:
        logger.exception(e)
        abort(400, str(e))
    except Exception as e:
        logger.exception(e)
        abort(500, str(e))

@bp.route('/all', methods=['GET'])
@jwt_admin_required()
def get_all_users():
    logger.info('Getting all users')
    try:
        user_list = user_service.get_all_users()
        user_dict_list = [user.model_dump(exclude='password') for user in user_list]
        response = jsonify(users=user_dict_list), 200

    except ValidationError as e:
        logger.exception(e)
        abort(400, str(e))
    except Exception as e:
        logger.exception(e)
        abort(500, str(e))
    
    return response 

@bp.route('/all', methods=['DELETE'])
@jwt_admin_required()
def delete_all_users():
    logger.info('Deleting all users')
    try:
        user_service.delete_all_users()
        return jsonify(msg="All users deleted"), 200
    
    except Exception as e:
        logger.exception(e)
        abort(500, str(e))