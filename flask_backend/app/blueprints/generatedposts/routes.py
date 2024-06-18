from bson import json_util
from flask import jsonify, abort
from flask_jwt_extended import get_current_user, jwt_required
from app.blueprints.generatedposts import bp, generated_post_service
from flask import request, make_response
from pydantic.json import pydantic_encoder
from app.models.generatedpost import GeneratedPost
from app.extensions import logger
from pydantic import ValidationError
from app.blueprints.admin_verification import jwt_admin_required

@bp.route('/generate', methods=['POST'])
@jwt_required()
def generate_post():
    logger.info('Generating post')
    try:
        user = get_current_user()
        prompt_data = request.get_json(silent=True)
        prompt_data['user_id'] = user.get_id()
        generated_post = generated_post_service.generate_post(**prompt_data)

        return jsonify(generated_post=generated_post.model_dump()), 200
    except KeyError as e:
        logger.exception(e)
        abort(404, str(e))
    except ValidationError as e:
        logger.exception(e)
        abort(400, str(e))
    except Exception as e:
        logger.exception(e)
        abort(500, str(e))

@bp.route('/posts/<string:post_id>', methods=['GET'])
@jwt_required()
def get_generated_post_by_post_id(post_id):
    logger.info(f'Getting generated post by post id {post_id}')
    try:
        current_user = get_current_user()
        
        if current_user is None:
            logger.error('No user found')
            return jsonify(error="No user found"), 400
        
        generated_post = generated_post_service.get_generated_post_by_id(post_id=post_id)
        logger.info(f'{generated_post=}')
        if generated_post is None:
            logger.error(f'Generated Post with ID {post_id} not found')
            return jsonify(error=f"Generated Post with ID {post_id} not found"), 404
        
        if str(generated_post.user_id) != current_user.get_id() and not current_user.is_admin():
            logger.error(f'User with ID {current_user.get_id()} does not have access to Generated Post with ID {post_id}')
            return jsonify(error=f"User with ID {current_user.get_id()} does not have access to Generated Post with ID {post_id}"), 403
        
        return jsonify(generated_post=generated_post.model_dump()), 200
    except Exception as e:
        logger.exception(e)
        abort(500, str(e))

@bp.route('/posts/history/<string:user_id>', methods=['GET'])
@jwt_required()
def get_user_generated_post_history(user_id):
    logger.info(f'Getting generated posts by user id {user_id}')
    try:
        current_user = get_current_user()
        if current_user is None:
                    logger.error('No user found')
                    return jsonify(error="No user found"), 400
        if current_user.get_id() != user_id and not current_user.is_admin():
            logger.error(f'User with ID {current_user.get_id()} does not have access to Generated Post for user ID {user_id}')
            return jsonify(error=f"User with ID {current_user.get_id()} does not have access to Generated Post for user ID {user_id}"), 403
        
        post_list = generated_post_service.get_generated_posts_by_user_id(user_id=user_id)
        
        return jsonify(generated_posts=[post.model_dump() for post in post_list]), 200
    except Exception as e:
        logger.exception(e)
        abort(500, str(e))
        
# admin commands

@bp.route('/posts/history/all', methods=['GET'])
@jwt_admin_required()
def get_all_generated_posts():
    logger.info('Getting all generated posts')
    try:
        post_list = generated_post_service.get_all_generated_posts()

        return jsonify(generated_posts=[post.model_dump() for post in post_list]), 200

    except Exception as e:
        logger.exception(e)
        abort(500, str(e))

@bp.route('/posts/history/all', methods=['DELETE'])
@jwt_admin_required()
def delete_all_generated_posts():
    logger.info('Deleting all generated posts')
    try:
        generated_post_service.delete_all_generated_posts()

        return jsonify(msg="All generated posts deleted successfully"), 200
    
    except Exception as e:
        logger.exception(e)
        abort(500, str(e))
