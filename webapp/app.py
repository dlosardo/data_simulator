import os
from flask import Flask
from webapp.extensions import debug_toolbar
from webapp.simulation.views import simulation_blueprint


config = {
    "development": "webapp.config.DevConfig",
    "testing": "webapp.config.TestingConfig",
    "default": "webapp.config.DevConfig"
}


def create_app(settings_override=None):
    """
    Create a Flask application using the app factory pattern.
    :param settings_override passed if default settings should be overidden
    :return Flask application instance
    """
    app = Flask(__name__, instance_relative_config=True)
    configure_app(app, settings_override)
    app.register_blueprint(simulation_blueprint)
    extensions(app)
    return app


def configure_app(app, settings_override):
    config_name = os.getenv('FLASK_CONFIG', 'default')
    app.config.from_object(config[config_name])
    app.config.from_pyfile(
        'config.cfg', silent=True)  # instance-folders config
    if settings_override:
        app.config.from_object(config[settings_override])
    return None


def extensions(app):
    """
    Register extensions (mutates the app passed in)
    :param app: Flask application instance
    :return None
    """
    debug_toolbar.init_app(app)
    return None
