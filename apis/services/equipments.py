from apis.models.equipment import equipment
from apis.models.vessel import vessel
from apis.models.model import db


class equipmentService:
    def insert_equipment(equipment_data):
        name = equipment_data.get("name")
        code = equipment_data.get("code")
        location = equipment_data.get("location")
        vessel_code = equipment_data.get("vessel_code")

        check_code_in_db = equipment.query.filter_by(code=code).first()
        if check_code_in_db is not None:
            return {"message": "REPEATED_CODE"}, 409
        
        check_vessel_code_in_db = vessel.query.filter_by(code=vessel_code).first()
        if check_vessel_code_in_db is None:
            return {"message": "NO_VESSEL"}, 409

        vessel_id = check_vessel_code_in_db.id

        new_equipment = equipment(
            code=code,
            name=name,
            location=location,
            vessel_id=vessel_id,
            active=True
          )
        db.session.add(new_equipment)
        db.session.commit()

        return {"message": "OK"}, 201
