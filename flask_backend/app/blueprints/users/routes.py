from bson import json_util
from flask import request, render_template, make_response, jsonify, flash, abort
from pydantic.json import pydantic_encoder
from pydantic import TypeAdapter, ValidationError
from app.blueprints.users import bp, user_service
from app.models.user import User
from app.models.user_role import UserRole
from flask_jwt_extended import jwt_required, get_current_user
from app.extensions import logger

@bp.route('/update', methods=['PUT'])
@jwt_required()
def update_user():
    logger.info('Updating user')
    try:
        user = get_current_user()
        if user is None:
            logger.error('No user found')
            return make_response({"error": "No user found"}, 400)
        
        user_data = request.get_json(silent=True)
        logger.info(f'{user_data=}')
        if user_data is None:
            logger.error('No JSON input for user update')
            return make_response({"error": "No JSON input for user update"}, 400)
        
        for invalid_key in ['id', 'email', 'role']:
            if invalid_key in user_data.keys() and user_data[invalid_key] != getattr(user, invalid_key):
                logger.error(f'Cannot set {invalid_key} for user update')
                return make_response({"error": f"Cannot set {invalid_key} for user update"}, 400)
        
        user = user_service.update_user(user.get_id(), User(**user_data))
        
        return jsonify({
                "message": "User updated successfully",
                "user": user.model_dump_json(by_alias=True, indent=4)
                }), 200
         
    except ValidationError as e:
        logger.exception(e)
        abort(400, str(e))
    except Exception as e:
        logger.exception(e)
        abort(500, str(e))

@bp.route('/all', methods=['GET'])
@jwt_required()
def get_all_users():
    try:
        user = get_current_user()
        if user.role != UserRole.ADMIN:
            logger.error('Unauthorized GET request to /users/all')
            return make_response({"error": "Unauthorized GET request to /users/all"}, 403)
        
        user_list = user_service.get_all_users()

        response = make_response({"users":json_util.dumps(user_list, default=pydantic_encoder)}, 200)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    return response 

@bp.route('/all', methods=['DELETE'])
@jwt_required()
def delete_all_users():
    try:
        user = get_current_user()
        if user.role != UserRole.ADMIN:
            logger.error('Unauthorized DELETE request to /users/all')
            return make_response({"error": "Unauthorized DELETE request to /users/all"}, 403)
        
        user_service.delete_all_users()
        response = make_response()
        response.status_code = 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    return response