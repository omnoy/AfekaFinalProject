from bson import json_util
from flask import request, make_response
from pydantic.json import pydantic_encoder
from pydantic import TypeAdapter
from app.blueprints.publicofficials import bp, public_official_service
from app.models.publicofficial import PublicOfficial

@bp.route('/', methods=['POST'])
def create_public_official():
    try:
        po_data = request.get_json(silent=True)
        if po_data is None:
            return make_response({"error": "Invalid JSON input"}, 400)
        
        public_official = PublicOfficial(**po_data)
        public_official = public_official_service.create_public_official(public_official)

        response = make_response((public_official.model_dump_json(by_alias=True, indent=4), 200))
    except Exception as e:
        return make_response({'error': str(e)}, 500)
    return response

@bp.route('/<string:po_id>', methods=['GET'])
def get_public_official_by_id(po_id):
    try:
        public_official = public_official_service.get_public_official_by_id(public_official_id=po_id)

        response = make_response((public_official.model_dump_json(by_alias=True, indent=4), 200))
    except Exception as e:
        return make_response({'error': str(e)}, 500)
    return response

#TODO this
@bp.route('/<string:po_id>', methods=['PUT'])
def update_public_official(po_id):
    pass

# admin commands

@bp.route('/public-officials', methods=['GET'])
def get_all_public_officials():
    po_list = public_official_service.get_all_public_officials()

    response = make_response((json_util.dumps(po_list, default=pydantic_encoder), 200))
    return response 

@bp.route('/public-officials', methods=['DELETE'])
def delete_all_public_officials():
    public_official_service.delete_all_public_officials()

    response = make_response()
    response.status_code = 200
    return response