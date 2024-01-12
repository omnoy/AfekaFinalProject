from flask import render_template
from app.publicofficials import bp
from app.extensions import mongo

# add json
@bp.route('/public-official', methods=['POST'])
def create_public_official():
    pass

@bp.route('/public-official/<string:po_id>', methods=['PUT'])
def update_public_official(po_id):
    pass

# admin commands

@bp.route('/public-official', methods=['GET'])
def get_all_public_officials():
    pass

@bp.route('/public-official', methods=['DELETE'])
def delete_all_public_officials():
    pass