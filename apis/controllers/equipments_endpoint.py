from flask import Blueprint, request
from apis.services.equipments import equipmentService
from apis.utils.response_message import MESSAGE

equipments_blueprint = Blueprint("equipments", __name__)


@equipments_blueprint.route("/insert_equipment", methods=["POST"])
def insert_equipment():
    """Insert a new equipment
    ---
    parameters:
        - name: body
          in: body
          required: true
          example: {
            vessel_code: string,
            code: string,
            location: string,
            name: string,
            }
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
    required_fields = ["name", "code", "location", "vessel_code"]

    body_keys = body.keys()
    for key in required_fields:
        if key not in body_keys:
            return MESSAGE["MISSING_PARAM"], 400

    for field in body:
        if not isinstance(body[field], str):
            return MESSAGE["WRONG_FORMAT"], 400
        if not len(body[field]):
            return MESSAGE["MISSING_PARAM"], 400

    create_equipment = equipmentService.insert_equipment(body)
    return create_equipment


@equipments_blueprint.route("/update_equipment_status", methods=["PUT"])
def update_equipment_status():
    """Set a equipment or a list of those to inactive
    ---
    parameters:
        - name: body
          in: body
          required: true
          example: {code: string}
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

    body = request.get_json()

    if "code" not in body:
        return MESSAGE["MISSING_PARAM"], 400

    codes = body.get("code")
    codes_is_list = isinstance(codes, list)

    if not codes_is_list:
        codes = [codes]

    if not len(codes):
        return MESSAGE["MISSING_PARAM"], 400

    for code in codes:
        if not isinstance(code, str):
            return MESSAGE["WRONG_FORMAT"], 400
        if not len(code) or not len(codes):
            return MESSAGE["MISSING_PARAM"], 400

    update_equipment = equipmentService.update_equipment_status(codes)
    return update_equipment


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
      409:
        description: returns NO_VESSEL if the vessel is not already in the system
    """

    query = request.args.get("vessel_code")

    if query is None:
        return MESSAGE["MISSING_PARAM"], 400

    list_equipments = equipmentService.active_equipment(query)

    return list_equipments


@equipments_blueprint.route("/list_equipments", methods=["GET"])
def list_equipment_by_name():
    """Return a list of equipments by name and which vessel it belongs
    ---
    parameters:
        - name: equipment_name
          in: query
          type: string
          required: true
    responses:
      200:
        description: returns a json with equipments key, a list of equipments and the vessel_code related
      400:
        description: returns MISSING_PARAMETER if the equipment_name is not sent
      409:
        description: returns NO_EQUIPMENT_NAME if the name is not already in the system
    """

    query = request.args.get("equipment_name")

    if query is None:
        return MESSAGE["MISSING_PARAM"], 400

    list_equipments = equipmentService.list_equipment_by_name(query)

    return list_equipments
