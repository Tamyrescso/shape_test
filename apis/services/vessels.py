from apis.models.model import db
from apis.models.vessel import vessel


class vesselsService:
    def insert_vessel(code):
        check_code_in_database = vessel.query.filter_by(code=code).first()

        if check_code_in_database is not None:
            return {"message": "FAIL"}, 409

        new_vessel = vessel(code=code)
        db.session.add(new_vessel)
        db.session.commit()

        return {"message": "OK"}, 201
