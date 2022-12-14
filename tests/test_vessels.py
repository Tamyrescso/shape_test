import pytest
from flask_migrate import Migrate
from sqlalchemy import func

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

from apis.app import create_app
from apis.models.model import db
from apis.models.vessel import vessel


@pytest.fixture(scope="module")
def app():
    app = create_app(test_config=True)

    with app.app_context():
        db.create_all()
        Migrate(app, db)

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


def test_insert_clean_db(app):
    result = app.test_client().post("/vessel/insert_vessel", json={"code": "MV102"})

    assert result.get_json().get("message") == "OK"
    assert result.status_code == 201
    with app.app_context():
        query = db.session.query(vessel.code)
        query_results = db.session.execute(query).all()
        assert query_results[0][0] == "MV102"


def test_insert_replicated(app):
    result = app.test_client().post("/vessel/insert_vessel", json={"code": "MV102"})

    assert result.get_json().get("message") == "FAIL"
    assert result.status_code == 409
    with app.app_context():
        query = db.session.query(func.count(vessel.code))
        query_results = db.session.execute(query).all()
        assert query_results[0][0] == 1


def test_insert_without_parameter_code_or_empty_value(app):
    scenarios = [
        {"code": ""},
        {"wrong": "MV102"},
    ]

    for scenario in scenarios:
        result = app.test_client().post("/vessel/insert_vessel", json=scenario)
        assert result.get_json().get("message") == "MISSING_PARAMETER"
        assert result.status_code == 400

    with app.app_context():
        query = db.session.query(func.count(vessel.code))
        query_results = db.session.execute(query).all()
        assert query_results[0][0] == 1


def test_insert_wrong_format(app):
    result = app.test_client().post("/vessel/insert_vessel", json={"code": 123})

    assert result.get_json().get("message") == "WRONG_FORMAT"
    assert result.status_code == 400
    with app.app_context():
        query = db.session.query(func.count(vessel.code))
        query_results = db.session.execute(query).all()
        assert query_results[0][0] == 1
