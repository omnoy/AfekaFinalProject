from bson import json_util
from flask import render_template
from app.generatedposts import bp, generated_post_service
from flask import request, make_response
from pydantic.json import pydantic_encoder
from app.models.generatedpost import GeneratedPost
from app.models.generationprompt import GenerationPrompt

@bp.route('/generated-posts/generate', methods=['POST'])
def generate_post():
    prompt_data = request.get_json(silent=True)
    prompt = GenerationPrompt(**prompt_data)
    generated_post = generated_post_service.generate_post(prompt)

    response = make_response((generated_post.model_dump_json(by_alias=True, indent=4), 200))
    return response

@bp.route('/generated-posts/<string:post_id>', methods=['GET'])
def get_generated_post_by_user_id(post_id):
    generated_post = generated_post_service.get_generated_post_by_id(post_id=post_id)

    response = make_response((generated_post.model_dump_json(by_alias=True, indent=4), 200))
    return response

@bp.route('/generated-posts/<string:user_id>', methods=['GET'])
def get_generated_post_by_user_id(user_id):
    post_list = generated_post_service.get_generated_posts_by_user_id(user_id=user_id)

    response = make_response((json_util.dumps(post_list, default=pydantic_encoder), 200))
    return response 

@bp.route('/generated-posts/<string:po_id>', methods=['GET'])
def get_generated_post_by_public_official_id(po_id):
    post_list = generated_post_service.get_generated_posts_by_user_id(po_id=po_id)

    response = make_response((json_util.dumps(post_list, default=pydantic_encoder), 200))
    return response 

# admin commands

@bp.route('/generated-posts', methods=['GET'])
def get_all_generated_posts():
    post_list = generated_post_service.get_all_generated_posts()

    response = make_response((json_util.dumps(post_list, default=pydantic_encoder), 200))
    return response 

@bp.route('/generated-posts', methods=['DELETE'])
def delete_all_generated_posts():
    generated_post_service.delete_all_generated_posts()

    response = make_response()
    response.status_code = 200
    return response
