import os
from utils import fix_path

basedir = os.path.abspath(os.path.dirname(__file__))

#app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db/belly_button_biodiversity.sqlite"
class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = 0
    SQLALCHEMY_RECORD_QUERIES = 1
    SQLALCHEMY_ECHO = 0


class ProductionConfig(Config):
    LOG_TO_STDOUT = 1
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///" + fix_path(basedir, "db/belly_button_biodiversity.sqlite"))


class DevelopmentConfig(Config):
    DEBUG = 1
    FLASK_DEBUG = 1
    SQLALCHEMY_ECHO = 1
    TEMPLATES_AUTO_RELOAD = 1
    SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DATABASE_URI", "sqlite:///" + fix_path(basedir, "db/belly_button_biodiversity.sqlite"))

config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}