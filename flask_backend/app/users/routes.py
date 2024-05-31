from bson import json_util
from flask import request, make_response, jsonify, flash, abort
from flask_login import login_user, logout_user, login_required
from pydantic.json import pydantic_encoder
from pydantic import TypeAdapter, ValidationError
from app.users import bp, user_service
from app.models.user import User
from app.form import LoginForm

# basic commands

@bp.route('/users', methods=['POST'])
def create_user():
    try:
        user_data = request.get_json(silent=True)
        if user_data is None:
            return abort(400, "No JSON input")
        
        user = User(**user_data)
        user = user_service.create_user(user)

        response = make_response((user.model_dump_json(by_alias=True, indent=4), 200))
    except ValidationError as e:
        return abort(400,  f"Invalid JSON input: {str(e)}")
    except Exception as e:
        return abort(500, str(e))
    
    return response

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = user_service.get_user_by_email(form.email.data)
        if user is None:
            abort(401, 'Invalid username or password')
        
        if user.check_password(form.password.data):
            login_user(user)
            return make_response((user.model_dump_json(by_alias=True, indent=4), 200)) 
    
    return make_response(jsonify("GET success"), 200) 
        
@bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return make_response(jsonify("logout success"), 200) 


# def login(user_email):
#     user = user_service.get_user_by_id(user_email=user_email)

#     response = make_response((user.model_dump_json(by_alias=True, indent=4), 200))
#     return response

@bp.route('/logout', methods=['POST'])


@bp.route('/users/<string:user_email>', methods=['PUT'])
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

@bp.route('/users', methods=['GET'])
def get_all_users():
    try:
        user_list = user_service.get_all_users()

        response = make_response((json_util.dumps(user_list, default=pydantic_encoder), 200))
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    return response 

@bp.route('/users', methods=['DELETE'])
def delete_all_users():
    try:
        user_service.delete_all_users()

        response = make_response()
        response.status_code = 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    return response
