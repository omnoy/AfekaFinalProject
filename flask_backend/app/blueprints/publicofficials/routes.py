from bson import json_util
from flask import Response, jsonify, request
from pydantic.json import pydantic_encoder
from pydantic import TypeAdapter, ValidationError
from app.blueprints.publicofficials import bp, public_official_service
from app.models.publicofficial import PublicOfficial
from flask_jwt_extended import jwt_required, get_current_user
from app.extensions import logger
from app.models.exceptions.object_already_exists_exception import ObjectAlreadyExistsException
from app.blueprints.jwt_user_verification import jwt_admin_required, jwt_user_required

@bp.route('/create', methods=['POST'])
@jwt_admin_required()
def create_public_official():
    logger.info("Creating public official")
    try:
        po_data = request.get_json(silent=True)
        if po_data is None:
            logger.error('No JSON input for public official creation')
            return jsonify(error="Invalid JSON input"), 400
        
        public_official = PublicOfficial(**po_data)
        public_official = public_official_service.create_public_official(public_official)

        return jsonify(public_official=public_official.model_dump()), 200  

    except ObjectAlreadyExistsException as e:
        logger.exception(e)
        return jsonify(error=str(e)), 409
    except ValidationError as e:
        logger.exception(e)
        return jsonify(error=str(e)), 400
    except Exception as e:
        logger.exception(e)
        return jsonify(error=str(e)), 500

@bp.route('/get/<string:public_official_id>', methods=['GET'])
@jwt_user_required()
def get_public_official_by_id(public_official_id: str):
    logger.info(f'Getting public official by ID {public_official_id}')
    try:
        public_official = public_official_service.get_public_official_by_id(public_official_id=public_official_id)
        if public_official is None:
            logger.error(f'Public Official with ID {public_official_id} not found')
            return jsonify(error=f"Public Official with ID {public_official_id} not found"), 404
        
        return jsonify(public_official=public_official.model_dump()), 200
    except ValidationError as e:
        logger.exception(e)
        return jsonify(error=str(e)), 400
    except Exception as e:
        logger.exception(e)
        return jsonify(error=str(e)), 500

@bp.route('/update/<string:public_official_id>', methods=['PUT'])
@jwt_admin_required()
def update_public_official(public_official_id):
    logger.info(f'Updating public official ({public_official_id=})')
    try:
        po_data = request.get_json(silent=True)
        logger.info(f'{po_data=}')

        if po_data is None:
            logger.error('No JSON input for public official update')
            return jsonify(msg="No JSON input for public official update"), 400
        
        if "id" in po_data.keys() and po_data["id"] != public_official_id:
            logger.error(f'Cannot set id for public official update')
            return jsonify(error=f"Cannot set id for public official update"), 400
        
        po = public_official_service.update_public_official(public_official_id, PublicOfficial(**po_data))
        
        if po is None:
            logger.error(f'Public Official with ID {public_official_id} not found')
            return jsonify(msg=f"Public Official with ID {public_official_id} not found"), 404

        return jsonify(public_official=po.model_dump()), 200
         
    except ValidationError as e:
        logger.exception(e)
        return jsonify(error=str(e)), 400
    except Exception as e:
        logger.exception(e)
        return jsonify(error=str(e)), 500

@bp.route('/all', methods=['GET'])
@jwt_admin_required()
def get_all_public_officials():
    logger.info('Getting all public officials')
    try:
        po_list = public_official_service.get_all_public_officials()
        
        po_dict_list = [po.model_dump() for po in po_list]

        response = jsonify(public_officials=po_dict_list), 200
        return response 
    except ValidationError as e:
        logger.exception(e)
        return jsonify(error=str(e)), 400
    except Exception as e:
        logger.exception(e)
        return jsonify(error=str(e)), 500

@bp.route('/all', methods=['DELETE'])
@jwt_admin_required()
def delete_all_public_officials():
    logger.info("Deleting all public officials")
    try:
        public_official_service.delete_all_public_officials()

        return Response(status=200)
    
    except ValidationError as e:
        logger.exception(e)
        return jsonify(error=str(e)), 400
    except Exception as e:
        logger.exception(e)
        return jsonify(error=str(e)), 500