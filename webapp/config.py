import os

# absolute path for the parent directory of the directory your file is in
basedir = os.path.abspath(os.path.join(
    os.path.dirname(__file__), os.path.pardir))


class Config(object):
    SECRET_KEY = '1bc33738bbf2e659e40dbc21f9f2ac5d'
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = False
    SERVER_NAME = "localhost:8000"
