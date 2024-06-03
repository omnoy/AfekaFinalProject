from bson import json_util
from flask import request, make_response, jsonify, flash, abort
from pydantic import ValidationError
from app.blueprints.auth import bp, user_service
from app.models.user import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

# basic commands

@bp.route('/register', methods=['POST'])
def register():
    try:
        user_data = request.get_json(silent=True)
        if user_data is None:
            return abort(400, "No JSON input")
        
        user = User(**user_data)
        user = user_service.create_user(user)

        access_token = create_access_token(identity=user.get_id())

        response =jsonify({
            "message": "User Registered successfully",
            "access_token": access_token,
            "user": user.model_dump_json(by_alias=True, exclude={"password_hash"}, indent=4)
            }), 200

        return response
    except ValidationError as e:
        return abort(400,  f"Invalid JSON input: {str(e)}")
    except Exception as e:
        return abort(500, str(e))
    
    

@bp.route('/login', methods=['GET', 'POST'])
def login():
    # form = LoginForm()
    # if form.validate_on_submit():
    #     user = user_service.get_user_by_email(form.email.data)
    #     if user is None:
    #         abort(401, 'Invalid username or password')
        
    #     if user.check_password(form.password.data):
    #         login_user(user)
    #         return make_response((user.model_dump_json(by_alias=True, indent=4), 200)) 
    #     else:
    #         abort(401, 'Invalid username or password')
    
    return make_response({'message':'success'}, 200) 
        
@bp.route('/logout', methods=['POST'])
def logout():
    return make_response(jsonify("logout success"), 200) 


# def login(user_email):
#     user = user_service.get_user_by_id(user_email=user_email)

#     response = make_response((user.model_dump_json(by_alias=True, indent=4), 200))
#     return response