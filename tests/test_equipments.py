import pytest
from flask_migrate import Migrate

# from sqlalchemy import func, or_

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

from apis.app import create_app
from apis.models.model import db
from apis.models.vessel import vessel
from apis.models.equipment import equipment


@pytest.fixture(scope="module")
def app():
    app = create_app(test_config=True)

    with app.app_context():
        db.create_all()
        Migrate(app, db)
        vessel_obj1 = vessel(code="MV102")
        vessel_obj2 = vessel(code="MV101")
        db.session.add(vessel_obj1)
        db.session.add(vessel_obj2)
        db.session.commit()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


def test_insert_clean_db(app):
    result = app.test_client().post(
        "/equipment/insert_equipment",
        json={
            "vessel_code": "MV102",
            "code": "5310B9D7",
            "location": "brazil",
            "name": "compressor",
        },
    )
    assert result.get_json().get("message") == "OK"
    assert result.status_code == 201
    with app.app_context():
        query = db.session.query(equipment)
        query_results = db.session.execute(query).all()
        assert len(query_results) == 1
        assert query_results[0][0].vessel_id == 1
        assert query_results[0][0].code == "5310B9D7"
        assert query_results[0][0].location == "brazil"
        assert query_results[0][0].active
        assert query_results[0][0].name == "compressor"


def test_insert_without_vessel_code(app):
    result = app.test_client().post(
        "/equipment/insert_equipment",
        json={"code": "5310B9D7", "location": "brazil", "name": "compressor"},
    )
    print(result.get_json())
    assert result.get_json().get("message") == "MISSING_PARAMETER"
    assert result.status_code == 400
    with app.app_context():
        query = db.session.query(equipment)
        query_results = db.session.execute(query).all()
        assert len(query_results) == 1


def test_insert_without_code(app):
    result = app.test_client().post(
        "/equipment/insert_equipment",
        json={
            "vessel_code": "MV102",
            "location": "brazil",
            "name": "compressor",
        },
    )
    assert result.get_json().get("message") == "MISSING_PARAMETER"
    assert result.status_code == 400
    with app.app_context():
        query = db.session.query(equipment)
        query_results = db.session.execute(query).all()
        assert len(query_results) == 1


def test_insert_without_location(app):
    result = app.test_client().post(
        "/equipment/insert_equipment",
        json={
            "vessel_code": "MV102",
            "code": "5310B9D7",
            "name": "compressor",
        },
    )
    assert result.get_json().get("message") == "MISSING_PARAMETER"
    assert result.status_code == 400
    with app.app_context():
        query = db.session.query(equipment)
        query_results = db.session.execute(query).all()
        assert len(query_results) == 1


def test_insert_without_name(app):
    result = app.test_client().post(
        "/equipment/insert_equipment",
        json={
            "vessel_code": "MV102",
            "code": "5310B9D7",
            "location": "brazil",
        },
    )
    assert result.get_json().get("message") == "MISSING_PARAMETER"
    assert result.status_code == 400
    with app.app_context():
        query = db.session.query(equipment)
        query_results = db.session.execute(query).all()
        assert len(query_results) == 1


def test_insert_with_empty_value(app):
    result = app.test_client().post(
        "/equipment/insert_equipment",
        json={
            "vessel_code": "MV102",
            "code": "",
            "location": "brazil",
            "name": "compressor",
        },
    )
    assert result.get_json().get("message") == "MISSING_PARAMETER"
    assert result.status_code == 400
    with app.app_context():
        query = db.session.query(equipment)
        query_results = db.session.execute(query).all()
        assert len(query_results) == 1


def test_insert_with_wrong_format(app):
    result = app.test_client().post(
        "/equipment/insert_equipment",
        json={
            "vessel_code": 123,
            "code": "5310B9D7",
            "location": "brazil",
            "name": "compressor",
        },
    )
    assert result.get_json().get("message") == "WRONG_FORMAT"
    assert result.status_code == 400
    with app.app_context():
        query = db.session.query(equipment)
        query_results = db.session.execute(query).all()
        assert len(query_results) == 1


def test_insert_with_existent_code(app):
    result = app.test_client().post(
        "/equipment/insert_equipment",
        json={
            "vessel_code": "MV102",
            "code": "5310B9D7",
            "location": "brazil",
            "name": "compressor",
        },
    )
    assert result.get_json().get("message") == "REPEATED_CODE"
    assert result.status_code == 409
    with app.app_context():
        query = db.session.query(equipment)
        query_results = db.session.execute(query).all()
        assert len(query_results) == 1


def test_insert_if_vessel_does_not_exist(app):
    result = app.test_client().post(
        "/equipment/insert_equipment",
        json={
            "vessel_code": "ZD123",
            "code": "5HJN7N",
            "location": "brazil",
            "name": "compressor",
        },
    )
    assert result.get_json().get("message") == "NO_VESSEL"
    assert result.status_code == 409
    with app.app_context():
        query = db.session.query(equipment)
        query_results = db.session.execute(query).all()
        assert len(query_results) == 1


def test_update_status_one_item(app):
    result = app.test_client().put(
        "/equipment/update_equipment_status",
        json={"code": "5310B9D7"},
    )
    assert result.get_json().get("message") == "OK"
    assert result.status_code == 201
    with app.app_context():
        query = db.session.query(equipment)
        query_results = db.session.execute(query).all()
        assert len(query_results) == 1
        assert query_results[0][0].active is False


def test_update_status_list(app):
    app.test_client().post(
        "/equipment/insert_equipment",
        json={
            "vessel_code": "MV101",
            "code": "531dfddf",
            "location": "china",
            "name": "compressor",
        },
    )

    result = app.test_client().put(
        "/equipment/update_equipment_status",
        json={"code": ["5310B9D7", "531dfddf"]},
    )
    assert result.get_json().get("message") == "OK"
    assert result.status_code == 201
    with app.app_context():
        query = db.session.query(equipment)
        query_results = db.session.execute(query).all()
        assert len(query_results) == 2
        assert query_results[0][0].active is False
        assert query_results[1][0].active is False


def test_update_if_code_is_not_sent(app):
    result = app.test_client().put(
        "/equipment/update_equipment_status",
        json={"wrong": "5310B9D7"},
    )
    assert result.get_json().get("message") == "MISSING_PARAMETER"
    assert result.status_code == 400
    with app.app_context():
        query = db.session.query(equipment)
        query_results = db.session.execute(query).all()
        assert len(query_results) == 2


def test_update_if_parameter_is_empty(app):
    scenarios = [
        {"code": ""},
        {"code": []},
        {"code": [""]},
    ]

    for scenario in scenarios:
        result = app.test_client().put(
            "/equipment/update_equipment_status",
            json=scenario,
        )
        assert result.get_json().get("message") == "MISSING_PARAMETER"
        assert result.status_code == 400

    with app.app_context():
        query = db.session.query(equipment)
        query_results = db.session.execute(query).all()
        assert len(query_results) == 2


def test_update_if_format_is_wrong(app):
    scenarios = [
        {"code": 123},
        {"code": [123, {}, []]},
        {"code": ["5310B9D7", 123]},
    ]

    for scenario in scenarios:
        result = app.test_client().put(
            "/equipment/update_equipment_status",
            json=scenario,
        )
        assert result.get_json().get("message") == "WRONG_FORMAT"
        assert result.status_code == 400

    with app.app_context():
        query = db.session.query(equipment)
        query_results = db.session.execute(query).all()
        assert len(query_results) == 2


def test_update_if_equipment_does_not_exist(app):
    scenarios = [
        {"code": "985F4RE"},
        {"code": ["5310B9D7", "985F4RE"]},
    ]

    for scenario in scenarios:
        result = app.test_client().put(
            "/equipment/update_equipment_status",
            json=scenario,
        )
        assert result.get_json().get("message") == "NO_CODE"
        assert result.status_code == 409

    with app.app_context():
        query = db.session.query(equipment)
        query_results = db.session.execute(query).all()
        assert len(query_results) == 2


def test_get_active_equipments_by_vessel(app):
    empty_result = app.test_client().get(
        "/equipment/active_equipments?vessel_code=MV102"
    )
    assert empty_result.get_json() == []
    assert empty_result.status_code == 200

    app.test_client().post(
        "/equipment/insert_equipment",
        json={
            "vessel_code": "MV102",
            "code": "531df345",
            "location": "china",
            "name": "compressor",
        },
    )

    result = app.test_client().get("/equipment/active_equipments?vessel_code=MV102")
    assert result.get_json() == [
        {
            "active": True,
            "code": "531df345",
            "id": 3,
            "location": "china",
            "name": "compressor",
        }
    ]
    assert result.status_code == 200
    with app.app_context():
        query = db.session.query(equipment)
        query_results = db.session.execute(query).all()
        assert len(query_results) == 3


def test_get_active_equipments_without_query_parameter(app):
    scenarios = [
        "/equipment/active_equipments",
        "/equipment/active_equipments?wrong=MV102",
    ]
    for scenario in scenarios:
        result = app.test_client().get(scenario)
        assert result.get_json().get("message") == "MISSING_PARAMETER"
        assert result.status_code == 400

    with app.app_context():
        query = db.session.query(equipment)
        query_results = db.session.execute(query).all()
        assert len(query_results) == 3


def test_get_active_equipments_if_vessel_does_not_exist(app):
    result = app.test_client().get("/equipment/active_equipments?vessel_code=MV103")
    assert result.get_json().get("message") == "NO_VESSEL"
    assert result.status_code == 409
    with app.app_context():
        query = db.session.query(equipment)
        query_results = db.session.execute(query).all()
        assert len(query_results) == 3


def test_get_equipments_by_name(app):
    result = app.test_client().get(
        "/equipment/list_equipments?equipment_name=compressor"
    )
    assert result.get_json() == [
        {
            "equipments_compressor": [
                {
                    "active": False,
                    "code": "5310B9D7",
                    "id": 1,
                    "location": "brazil",
                    "name": "compressor",
                },
                {
                    "active": True,
                    "code": "531df345",
                    "id": 3,
                    "location": "china",
                    "name": "compressor",
                },
            ],
            "vessel_code": "MV102",
        },
        {
            "equipments_compressor": [
                {
                    "active": False,
                    "code": "531dfddf",
                    "id": 2,
                    "location": "china",
                    "name": "compressor",
                }
            ],
            "vessel_code": "MV101",
        },
    ]
    assert result.status_code == 200
    with app.app_context():
        query = db.session.query(equipment)
        query_results = db.session.execute(query).all()
        assert len(query_results) == 3


def test_get_equipments_by_name_without_query_parameter(app):
    scenarios = [
        "/equipment/list_equipments",
        "/equipment/list_equipments?wrong=MV102",
    ]
    for scenario in scenarios:
        result = app.test_client().get(scenario)
        assert result.get_json().get("message") == "MISSING_PARAMETER"
        assert result.status_code == 400

    with app.app_context():
        query = db.session.query(equipment)
        query_results = db.session.execute(query).all()
        assert len(query_results) == 3


def test_get_equipments_by_name_if_does_not_exist(app):
    result = app.test_client().get("/equipment/list_equipments?equipment_name=motor")
    assert result.get_json().get("message") == "NO_EQUIPMENT_NAME"
    assert result.status_code == 409
    with app.app_context():
        query = db.session.query(equipment)
        query_results = db.session.execute(query).all()
        assert len(query_results) == 3
