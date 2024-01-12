from flask import render_template, jsonify, request
from app.users import bp, user_service
from app.models.user import User

# basic commands

# add json
@bp.route('/users', methods=['POST'])
def create_user():
    user_data = request.get_json(silent=True)
    user = User(**user_data)
    user_id = user_service.create_user(user)
    return str(user_id)

@bp.route('/users/login/<string:user_id>', methods=['GET'])
def login(user_id):
    return user_service.get_user_by_id(user_id=user_id)

@bp.route('/users/update/<string:user_id>', methods=['PUT'])
def update_user(user_id):
    pass

# admin commands

@bp.route('/users', methods=['GET'])
def get_all_users():
    return user_service.get_all_users()

@bp.route('/users', methods=['DELETE'])
def delete_all_users():
    pass