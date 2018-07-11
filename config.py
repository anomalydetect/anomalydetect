import os
from utils import fix_path

basedir = os.path.abspath(os.path.dirname(__file__))

#app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db/belly_button_biodiversity.sqlite"
class Config(object):
    UPLOAD_BASE = 'db/data/'



class ProductionConfig(Config):
	LOG_TO_STDOUT = 1
	UPLOAD_BASE = 'db/data/'


class DevelopmentConfig(Config):
	DEBUG = 1
	FLASK_DEBUG = 1
	TEMPLATES_AUTO_RELOAD = 1
	UPLOAD_BASE = 'db/data/'

config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}