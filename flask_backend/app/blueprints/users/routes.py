from bson import json_util
from flask import request, render_template, make_response, jsonify, flash, abort
from pydantic.json import pydantic_encoder
from pydantic import TypeAdapter, ValidationError
from app.blueprints.users import bp, user_service
from app.models.user import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

# basic commands
@bp.route('/<string:user_email>', methods=['GET'])
def get_user(user_email):
    try:
        user = user_service.get_user_by_id(user_email=user_email)
        response = make_response((user.model_dump_json(by_alias=True, indent=4), 200))

    except ValidationError as e:
        return jsonify({"error": "Invalid JSON input", "message": str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return response 

@bp.route('/<string:user_email>', methods=['PUT'])
def update_user(user_email):
    try:
        user_data = request.get_json(silent=True)
        if user_data is None:
            return make_response({"error": "Invalid JSON input"}, 400)
        
        ta = TypeAdapter(User)
        print(ta.validate_python(user_data))
        user = user_service.update_user(user_email, user)
        
        response = make_response((user.model_dump_json(by_alias=True, indent=4), 200))
    except ValidationError as e:
        return jsonify({"error": "Invalid JSON input", "message": str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return response 

# admin commands

@bp.route('/', methods=['GET'])
def get_all_users():
    try:
        user_list = user_service.get_all_users()

        response = make_response((json_util.dumps(user_list, default=pydantic_encoder), 200))
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    return response 

@bp.route('/', methods=['DELETE'])
def delete_all_users():
    try:
        user_service.delete_all_users()

        response = make_response()
        response.status_code = 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    return response
