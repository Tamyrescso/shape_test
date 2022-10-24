from flask import jsonify
from apis.models.equipment import equipment
from apis.models.vessel import vessel
from apis.models.model import db
from apis.utils.response_message import MESSAGE


class equipmentService:
    def insert_equipment(equipment_data):
        name = equipment_data.get("name")
        code = equipment_data.get("code")
        location = equipment_data.get("location")
        vessel_code = equipment_data.get("vessel_code")

        check_code_in_db = equipment.query.filter_by(code=code).first()
        if check_code_in_db is not None:
            return MESSAGE["REPEATED_CODE"], 409

        check_vessel_code_in_db = vessel.query.filter_by(code=vessel_code).first()
        if check_vessel_code_in_db is None:
            return MESSAGE["NO_VESSEL"], 409

        vessel_id = check_vessel_code_in_db.id

        new_equipment = equipment(
            code=code, name=name, location=location, vessel_id=vessel_id, active=True
        )
        db.session.add(new_equipment)
        db.session.commit()

        return MESSAGE["OK"], 201

    def update_equipment_status(codes):
        for code in codes:
            check_code_in_db = equipment.query.filter_by(code=code).first()

            if check_code_in_db is None:
                return MESSAGE["NO_CODE"], 409
            else:
                check_code_in_db.active = False

        db.session.commit()

        return MESSAGE["OK"], 201

    def active_equipment(vessel_code):
        check_vessel_code_in_db = vessel.query.filter_by(code=vessel_code).first()

        if check_vessel_code_in_db is None:
            return MESSAGE["NO_VESSEL"], 409

        vessel_id = check_vessel_code_in_db.id

        active_equipments_by_vessel = equipment.query.filter_by(
            active=True, vessel_id=vessel_id
        ).all()

        list_equipments = []
        for eq in active_equipments_by_vessel:
            list_equipments.append(
                {
                    "id": eq.id,
                    "name": eq.name,
                    "code": eq.code,
                    "location": eq.location,
                    "active": eq.active,
                }
            )

        return jsonify(list_equipments), 200

    def list_equipment_by_name(equipment_name):
        check_name_in_db = equipment.query.filter_by(name=equipment_name).first()

        if check_name_in_db is None:
            return MESSAGE["NO_EQUIPMENT_NAME"], 409

        list_by_name = (
            db.session.query(equipment, vessel)
            .join(vessel)
            .filter(equipment.name == equipment_name)
        )

        equipments_collection = {}
        for equip_obj, vessel_obj in list_by_name:
            equip = {
                "id": equip_obj.id,
                "name": equip_obj.name,
                "code": equip_obj.code,
                "location": equip_obj.location,
                "active": equip_obj.active,
            }

            if equipments_collection.get(vessel_obj.code):
                equipments_collection[vessel_obj.code].append(equip)
            else:
                equipments_collection[vessel_obj.code] = [equip]

        formatted_equipments_list = []
        for key in equipments_collection:
            formatted_equipments_list.append(
                {
                    "vessel_code": key,
                    f"equipments_{equipment_name}": equipments_collection[key],
                }
            )

        return jsonify(formatted_equipments_list), 200
