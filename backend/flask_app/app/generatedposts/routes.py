from flask import render_template
from app.generatedposts import bp
from app.extensions import mongo

# add json
@bp.route('/generate-post', methods=['POST'])
def generate_post():
    pass

@bp.route('/generate-post/<string:user_id>', methods=['GET'])
def get_generated_post_by_user_id():
    pass

@bp.route('/generate-post/<string:po_id>', methods=['GET'])
def get_generated_post_by_po_id():
    pass

# admin commands

@bp.route('/generate-post', methods=['GET'])
def get_all_generated_posts():
    pass

@bp.route('/generate-post', methods=['DELETE'])
def delete_all_generated_posts():
    pass
