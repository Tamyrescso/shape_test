from flask import Flask
from flasgger import Swagger

from apis.models.model import db
from apis.healthcheck import healthcheck_blueprint
from apis.controllers.vessels_endpoint import vessels_blueprint
from apis.controllers.equipments_endpoint import equipments_blueprint


def create_app(app_name="VESSELS", test_config=False, production_conf=False):
    app = Flask(app_name)
    Swagger(app)
    if test_config:
        app.config.from_object("config.TestConfig")
    else:
        app.config.from_object("config.RunConfig")

    # Register api blueprints
    app.register_blueprint(healthcheck_blueprint)
    app.register_blueprint(vessels_blueprint, url_prefix="/vessel")
    app.register_blueprint(equipments_blueprint, url_prefix="/equipment")

    db.init_app(app)

    return app


# if __name__ == "__main__":
#    app = create_app(production_conf=False)
#    app.run(host="0.0.0.0", port='5000', debug=True)
