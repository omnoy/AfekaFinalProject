from flask import Response, jsonify
from flask_jwt_extended import get_current_user, jwt_required
from app.blueprints.generatedposts import bp, generated_post_service
from flask import request
from app.extensions import logger
from app.blueprints.jwt_user_verification import jwt_admin_required, jwt_user_required
from app.models.exceptions.post_generation_failure_exception import PostGenerationFailureException

@bp.route('/generate', methods=['POST'])
@jwt_user_required()
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
        return jsonify(error=str(e)), 404
    except ValueError as e:
        logger.exception(e)
        return jsonify(error=str(e)), 400
    except PostGenerationFailureException as e:
        logger.exception(e)
        return jsonify(error=str(e)), 422
    except Exception as e:
        logger.exception(e)
        return jsonify(error=str(e)), 500

@bp.route('/posts/<string:post_id>', methods=['GET'])
@jwt_user_required()
def get_generated_post_by_post_id(post_id: str):
    logger.info(f'Getting generated post by post id {post_id}')
    try:
        current_user = get_current_user()
        
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
        return jsonify(error=str(e)), 500

@bp.route('/posts/user', methods=['GET'])
@jwt_user_required()
def get_user_generated_post_history():
    logger.info(f'Getting generated posts by user id')
    try:
        current_user = get_current_user()

        post_list = generated_post_service.get_generated_posts_by_user_id(user_id=current_user.get_id())
        
        return jsonify(generated_posts=[post.model_dump() for post in post_list]), 200
    except Exception as e:
        logger.exception(e)
        return jsonify(error=str(e)), 500
        
# admin commands

@bp.route('/posts/all', methods=['GET'])
@jwt_admin_required()
def get_all_generated_posts():
    logger.info('Getting all generated posts')
    try:
        post_list = generated_post_service.get_all_generated_posts()

        return jsonify(generated_posts=[post.model_dump() for post in post_list]), 200

    except Exception as e:
        logger.exception(e)
        return jsonify(error=str(e)), 500

@bp.route('/posts/all', methods=['DELETE'])
@jwt_admin_required()
def delete_all_generated_posts():
    logger.info('Deleting all generated posts')
    try:
        generated_post_service.delete_all_generated_posts()

        return Response(status=200)
    
    except Exception as e:
        logger.exception(e)
        return jsonify(error=str(e)), 500
