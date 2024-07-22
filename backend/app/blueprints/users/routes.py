from flask import Response, request, jsonify
from pydantic import ValidationError
from app.blueprints.users import bp, user_service, public_official_service, generated_post_service
from app.models.exceptions.object_id_not_found_exception import ObjectIDNotFoundException
from app.models.user import User
from flask_jwt_extended import get_current_user
import logging
from app.blueprints.jwt_user_verification import jwt_admin_required, jwt_user_required

@bp.route('/get', methods=['GET'])
@jwt_user_required()
def get_user():
    logging.info('Getting user')
    try:
        user = get_current_user()
        
        return jsonify(user=user.model_dump(exclude='password')), 200
    except Exception as e:
        logging.exception(e)
        return jsonify(error=str(e)), 500


@bp.route('/update', methods=['PUT'])
@jwt_user_required()
def update_user():
    logging.info('Updating user')
    try:
        user = get_current_user()
        
        user_update_data = request.get_json(silent=True)
        logging.info(f'{user_update_data=}')
        if user_update_data is None:
            logging.error('No JSON input for user update')
            return jsonify(error="No JSON input for user update"), 400
        
        if all([user_update_item in user.model_dump().items() for user_update_item in user_update_data.items()]):
            return jsonify(user=user.model_dump()), 200
        
        for invalid_key in ['id', 'password', 'email', 'role']:
            if invalid_key in user_update_data.keys() and user_update_data[invalid_key] != getattr(user, invalid_key):
                logging.error(f'Cannot set {invalid_key} for user update')
                return jsonify(error=f"Cannot set {invalid_key} for user update"), 400
        
        updated_user = user.model_copy(update=user_update_data)
        updated_user.model_validate(updated_user, strict=True)
        
        logging.info(f'{updated_user=}')
        user = user_service.update_user(user.get_id(), updated_user)
        
        return jsonify(user=user.model_dump()), 200
         
    except ValidationError as e:
        logging.exception(e)
        return jsonify(error=str(e)), 400
    except Exception as e:
        logging.exception(e)
        return jsonify(error=str(e)), 500

@bp.route('/favorites/<string:favorite_type>', methods=['GET'])
@jwt_user_required()
def get_user_favorites(favorite_type: str):
    logging.info('Add user')
    try:
        user = get_current_user()
        
        service_retrieval_function = None
        if favorite_type == 'public_official': 
            service_retrieval_function = public_official_service.get_public_official_by_id_list
        elif favorite_type == 'generated_post':
            service_retrieval_function = generated_post_service.get_generated_post_by_id_list
        else:
            logging.error('Invalid favorite type')
            return jsonify(error="Invalid favorite type"), 404
        
        favorite_ids = user_service.get_favorite_ids(favorite_type, user.get_id())
        
        favorites = service_retrieval_function(favorite_ids)
        
        favorite_dicts = [favorite.model_dump() for favorite in favorites]
        
        return jsonify(favorites=favorite_dicts), 200
    except ObjectIDNotFoundException as e:
        logging.exception(e)
        return jsonify(error=str(e)), 404
    except KeyError as e:
        logging.exception(f"Invalid favorite type given: {favorite_type}")
        return jsonify(error=f"Invalid favorite type given: {favorite_type}"), 400
    except Exception as e:
        logging.exception(e)
        return jsonify(error=str(e)), 500

@bp.route('/favorites/<string:favorite_type>/<string:object_id>', methods=['PUT'])
@jwt_user_required()
def add_to_favorites(favorite_type: str, object_id: str):
    logging.info('Add favorite to user')
    try:
        user = get_current_user()

        service_retrieval_function = None
        if favorite_type == 'public_official': 
            service_retrieval_function = public_official_service.get_public_official_by_id
        elif favorite_type == 'generated_post':
            service_retrieval_function = generated_post_service.get_generated_post_by_id
        else:
            logging.error('Invalid favorite type')
            return jsonify(error="Invalid favorite type"), 404

        retrieved_object = service_retrieval_function(object_id)

        if not retrieved_object:
            logging.error(f'Favorite {favorite_type} with ID {object_id} not found')
            return jsonify(error=f"Favorite {favorite_type} with ID {object_id} not found"), 404

        if favorite_type == 'generated_post' and str(retrieved_object.user_id) != user.get_id():
            logging.error(f'User with ID {user.get_id()} does not have permission to favorite this post')
            return jsonify(error=f"User with ID {user.get_id()} does not have permission to favorite this post"), 403

        user_service.add_favorite(favorite_type, user.get_id(), object_id)
        
        return Response(status=200)
    except ObjectIDNotFoundException as e:
        logging.exception(e)
        return jsonify(error=str(e)), 404
    except KeyError as e:
        logging.exception(f"Invalid favorite type given: {favorite_type}")
        return jsonify(error=f"Invalid favorite type given: {favorite_type}")
    except ValueError as e:
        logging.exception(f"User does not have permission to favorite this post")
        return jsonify(error=f"User does not have permission to favorite this post"), 403
    except Exception as e:
        logging.exception(e)
        return jsonify(error=str(e)), 500

@bp.route('/favorites/<string:favorite_type>/<string:object_id>', methods=['DELETE'])
@jwt_user_required()
def remove_from_favorites(favorite_type: str, object_id: str):
    logging.info('Removing favorite from user')
    try:
        user = get_current_user()
        
        service_retrieval_function = None
        if favorite_type == 'public_official': 
            service_retrieval_function = public_official_service.get_public_official_by_id
        elif favorite_type == 'generated_post':
            service_retrieval_function = generated_post_service.get_generated_post_by_id
        else:
            logging.error('Invalid favorite type')
            return jsonify(error="Invalid favorite type"), 404

        if not service_retrieval_function(object_id):
            logging.error(f'Favorite {favorite_type} with ID {object_id} not found')
            return jsonify(error=f"Favorite {favorite_type} with ID {object_id} not found"), 404

        user_service.remove_favorite(favorite_type, user.get_id(), object_id)
        
        return Response(status=200)
    except ObjectIDNotFoundException as e:
        logging.exception(e)
        return jsonify(error=str(e)), 404
    except KeyError as e:
        logging.exception(f"Invalid favorite type given: {favorite_type}")
        return jsonify(error=f"Invalid favorite type given: {favorite_type}"), 400
    except ValueError as e:
        logging.exception(f"User does not have permission to remove this post from favorites")
        return jsonify(error=f"User does not have permission to remove this post from favorites"), 403
    except Exception as e:
        logging.exception(e)
        return jsonify(error=str(e)), 500

@bp.route('/all', methods=['GET'])
@jwt_admin_required()
def get_all_users():
    logging.info('Getting all users')
    try:
        user_list = user_service.get_all_users()
        user_dict_list = [user.model_dump(exclude='password') for user in user_list]
        return jsonify(users=user_dict_list), 200

    except ValidationError as e:
        logging.exception(e)
        return jsonify(error=str(e)), 400
    except Exception as e:
        logging.exception(e)
        return jsonify(error=str(e)), 500

@bp.route('/all', methods=['DELETE'])
@jwt_admin_required()
def delete_all_users():
    logging.info('Deleting all users')
    try:
        user_service.delete_all_users()
        return Response(status=200)
    
    except Exception as e:
        logging.exception(e)
        return jsonify(error=str(e)), 500