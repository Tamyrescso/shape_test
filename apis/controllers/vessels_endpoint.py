from flask import Blueprint, request
from apis.services.vessels import vesselsService

vessels_blueprint = Blueprint("vessels", __name__)


@vessels_blueprint.route("/insert_vessel", methods=["POST"])
def insert_vessel():
    """Insert a new vessel
    ---
    parameters:
        - name: code
          in: body
          type: string
          required: true
    responses:
        201:
          description: returns OK if the vessel was correctly inserted
        400:
          description: returns MISSING_PARAMETER if the vessel code is not sent
        400:
          description: returns WRONG_FORMAT if any parameter are sent in the wrong format
        409:
          description: returns FAIL if the vessel code is already in the system
    """

    body = request.get_json()

    if "code" not in body:
        return {"messsage": "MISSING_PARAMETER"}, 400

    code = body.get("code")
    if len(code) == 0:
        return {"messsage": "MISSING_PARAMETER"}, 400
    if type(code) is not str:
        return {"messsage": "WRONG_FORMAT"}, 400

    create_vessel = vesselsService.insert_vessel(code)
    return create_vessel
