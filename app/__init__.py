"""Creating app"""
import os
from flask import Flask
from instance.config import app_config

from .api.v1.views.meetup_views import v1_meetup_blueprint
from .api.v1.views.questions_views import v1_question_blueprint
from .api.v1.views.auth_views import v1_auth_blueprint
from .api.v2.views.auth_views import v2_auth
from .api.v2.views.meetup_views import v2_meetup


def create_app(config_name):
    """creating  the app using the configurations in the dictionary created in the .config file"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')


    """register v1 blueprints"""
    app.register_blueprint(v1_meetup_blueprint)
    app.register_blueprint(v1_question_blueprint)
    app.register_blueprint(v1_auth_blueprint)

    app.register_blueprint(v2_auth)
    app.register_blueprint(v2_meetup)


    return app
