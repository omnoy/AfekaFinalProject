from flask import Response, request, jsonify, abort
from pydantic import ValidationError
from app.blueprints.users import bp, user_service
from app.models.exceptions.object_id_not_found_exception import ObjectIDNotFoundException
from app.models.user import User
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
        
        return jsonify(user=user.model_dump()), 200
         
    except ValidationError as e:
        logger.exception(e)
        abort(400, str(e))
    except Exception as e:
        logger.exception(e)
        abort(500, str(e))

@bp.route('/favorites/<string:favorite_type>', methods=['GET'])
@jwt_required()
def get_user_favorites(favorite_type: str):
    logger.info('Add user')
    try:
        user = get_current_user()
        if user is None:
            logger.error('No user found')
            return jsonify(msg="No user found"), 404
        
        if favorite_type not in ['public_official', 'generated_post']:
            logger.error('Invalid favorite type')
            return jsonify(error="Invalid favorite type"), 400
        
        favorites = [favorite.model_dump() for favorite in user_service.get_favorites(favorite_type, user.get_id())]
        
        return jsonify(favorites=favorites), 200
    except ObjectIDNotFoundException as e:
        logger.exception(e)
        abort(400, str(e))
    except KeyError as e:
        logger.exception(f"Invalid favorite type given: {favorite_type}")
        abort(400, f"Invalid favorite type given: {favorite_type}")
    except Exception as e:
        logger.exception(e)
        abort(500, str(e))

@bp.route('/favorites/<string:favorite_type>/<string:object_id>', methods=['PUT'])
@jwt_required()
def add_to_favorites(favorite_type: str, object_id: str):
    logger.info('Add favorite to user')
    try:
        user = get_current_user()
        if user is None:
            logger.error('No user found')
            return jsonify(msg="No user found"), 404
        
        if favorite_type not in ['public_official', 'generated_post']:
            logger.error('Invalid favorite type')
            return jsonify(error="Invalid favorite type"), 400

        user_service.add_favorite(favorite_type, user.get_id(), object_id)
        
        return Response(status=200)
    except ObjectIDNotFoundException as e:
        logger.exception(e)
        abort(400, str(e))
    except KeyError as e:
        logger.exception(f"Invalid favorite type given: {favorite_type}")
        abort(400, f"Invalid favorite type given: {favorite_type}")
    except ValueError as e:
        logger.exception(f"User does not have permission to favorite this post")
        abort(403, f"User does not have permission to favorite this post")
    except Exception as e:
        logger.exception(e)
        abort(500, str(e))

@bp.route('/favorites/<string:favorite_type>/<string:object_id>', methods=['DELETE'])
@jwt_required()
def remove_from_favorites(favorite_type: str, object_id: str):
    logger.info('Removing favorite from user')
    try:
        user = get_current_user()
        if user is None:
            logger.error('No user found')
            return jsonify(msg="No user found"), 404
        
        if favorite_type not in ['public_official', 'generated_post']:
            logger.error('Invalid favorite type')
            return jsonify(error="Invalid favorite type"), 400

        user_service.remove_favorite(favorite_type, user.get_id(), object_id)
        
        return Response(status=200)
    except ObjectIDNotFoundException as e:
        logger.exception(e)
        abort(400, str(e))
    except KeyError as e:
        logger.exception(f"Invalid favorite type given: {favorite_type}")
        abort(400, f"Invalid favorite type given: {favorite_type}")
    except ValueError as e:
        logger.exception(f"User does not have permission to favorite this post")
        abort(403, f"User does not have permission to favorite this post")
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
        return jsonify(users=user_dict_list), 200

    except ValidationError as e:
        logger.exception(e)
        abort(400, str(e))
    except Exception as e:
        logger.exception(e)
        abort(500, str(e))

@bp.route('/all', methods=['DELETE'])
@jwt_admin_required()
def delete_all_users():
    logger.info('Deleting all users')
    try:
        user_service.delete_all_users()
        return Response(status=200)
    
    except Exception as e:
        logger.exception(e)
        abort(500, str(e))