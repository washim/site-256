import os

class Config(object):
    SECRET_KEY = 'sdfl324safnk56ldkcnad456nsdsk565afduejfgcfht'
    
class DevConfig(object):
    DEBUG = True
    SECRET_KEY = 'sdfl324safnk56ldkcnad456nsdsk565afduejfgcfht'
    SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"
    ENV = os.environ.get("FLASK_ENV", "Dev")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DATABASE = "data.db"