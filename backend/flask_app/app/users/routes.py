from bson import json_util
from flask import request, make_response
from pydantic.json import pydantic_encoder
from pydantic import TypeAdapter
from app.users import bp, user_service
from app.models.user import User

# basic commands

@bp.route('/users', methods=['POST'])
def create_user():
    user_data = request.get_json(silent=True)
    user = User(**user_data)
    user = user_service.create_user(user)

    response = make_response((user.model_dump_json(by_alias=True, indent=4), 200))
    return response

@bp.route('/users/login/<string:user_id>', methods=['GET'])
def login(user_id):
    user = user_service.get_user_by_id(user_id=user_id)

    response = make_response((user.model_dump_json(by_alias=True, indent=4), 200))
    return response

#TODO this
@bp.route('/users/<string:user_id>', methods=['PUT'])
def update_user(user_id):
    user_data = request.get_json(silent=True)
    ta = TypeAdapter(User)
    print(ta.validate_python(user_data))
    user = user_service.update_user(user_id, user)
    
    response = make_response((user.model_dump_json(by_alias=True, indent=4), 200))
    return response 

# admin commands

@bp.route('/users', methods=['GET'])
def get_all_users():
    user_list = user_service.get_all_users()

    response = make_response((json_util.dumps(user_list, default=pydantic_encoder), 200))
    return response 

@bp.route('/users', methods=['DELETE'])
def delete_all_users():
    user_service.delete_all_users()

    response = make_response()
    response.status_code = 200
    return response
