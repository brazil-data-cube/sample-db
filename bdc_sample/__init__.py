import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from bdc_sample.blueprint import bp
from bdc_sample.config import get_settings
from bdc_sample.models import db


flask_bcrypt = Bcrypt()


def create_app(config_name):
    """
    Creates Brazil Data Cube WTSS application from config object
    Args:
        config_name (string|bdc_sample.config.Config) Config instance
    Returns:
        Flask Application with config instance scope
    """

    app = Flask(__name__)

    with app.app_context():
        app.config.from_object(config_name)
        app.register_blueprint(bp)
        db.init_model(app.config.get('SQLALCHEMY_URI'))


        flask_bcrypt.init_app(app)

    return app


app = create_app(
    get_settings(os.environ.get('ENVIRONMENT', 'DevelopmentConfig')))

CORS(app, resorces={r'/d/*': {"origins": '*'}})