from flask import Blueprint, request, jsonify
from sqlalchemy import func, extract, and_
from apis.services.equipments import equipmentService


equipments_blueprint = Blueprint("equipments", __name__)


@equipments_blueprint.route("/insert_equipment", methods=["POST"])
def insert_equipment():
    """Insert a new equipment
    ---
    parameters:
        - name: vessel_code
          in: body
          type: string
          required: true
        - name: code
          in: body
          type: string
          required: true
        - name: name
          in: body
          type: string
          required: true
        - name: location
          in: body
          type: string
          required: true
    responses:
      201:
        description: returns OK if the equipment was correctly inserted
      400:
        description: returns MISSING_PARAMETER if any parameter is not sent
      400:
        description: returns WRONG_FORMAT if any parameter are sent in the wrong format
      409:
        description: returns REPEATED_CODE if the equipment code is already in the system
      409:
        description: returns NO_VESSEL if the vessel code is not already in the system
    """

    body = request.get_json()
    required_fields = ['name', 'code', 'location', 'vessel_code']

    body_keys = body.keys()
    for key in required_fields:
        if key not in body_keys:
            return {"messsage": "MISSING_PARAMETER"}, 400

    for field in body:
        if len(body[field]) == 0:
            return {"messsage": "MISSING_PARAMETER"}, 400
        if type(body[field]) is not str:
            return {"messsage": "WRONG_FORMAT"}, 400

    create_equipment = equipmentService.insert_equipment(body)
    return create_equipment


@equipments_blueprint.route("/update_equipment_status", methods=["PUT"])
def update_equipment_status():
    """Set a equipment or a list of those to inactive
    ---
    parameters:
        - name: code
          in: body
          type: string
          required: true
    responses:
      201:
        description: returns OK if the equipments were correctly updated
      400:
        description: returns MISSING_PARAMETER if any parameter is not sent
      400:
        description: returns WRONG_FORMAT if any parameter are sent in the wrong format
      409:
        description: returns NO_CODE if the equipment code is not already in the system
    """
    return {"message": "OK"}, 201


@equipments_blueprint.route("/active_equipments", methods=["GET"])
def active_equipment():
    """Return the list of active equipments of a vessel
    ---
    parameters:
        - name: vessel_code
          in: query
          type: string
          required: true
    responses:
      200:
        description: returns a json with equipments key and a list of equipments
      400:
        description: returns MISSING_PARAMETER if the vessel_code is not sent
      400:
        description: returns WRONG_FORMAT if any parameter are sent in the wrong format
      409:
        description: returns NO_VESSEL if the vessel is not already in the system
    """
    return {"message": "OK"}, 200
