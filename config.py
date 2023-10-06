from pathlib import Path
from dotenv import load_dotenv, find_dotenv
import os
import redis
from datetime import timedelta
import json

env_path =Path(".", ".env") #env path

load_dotenv(find_dotenv())

class Config:
    SQLALCHEMY_TRACK_MODIFICATION = False

    @staticmethod
    def init_app(app):
        pass

class DatabaseConfig(Config):
    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_USER =  os.getenv('MYSQL_USER')
    MYSQL_PASSWORD =  os.getenv('MYSQL_PASSWORD')
    MYSQL_DB =  os.getenv('MYSQL_DB')

class SessionConfig(Config):
    SESSION_REDIS = redis.from_url('redis://127.0.0.1:6379')
    SESSION_TYPE = 'redis'
    SESSION_USE_SIGNER = True
    SESSION_PERMANENT = False
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=60)

class MailConig(Config):
    MAIL_SERVER ='smtp.mailosaur.net'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

class FileUpload(Config):
    '''
    File Upload COnfiguration
    '''
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENTIONS = {'txt', 'jpg', 'png', 'jpeg'}
    MAX_CONTENT_LENGTH = 5 * 1000 * 1000

class dbMongo(Config):
    MONGO_URI = os.environ.get("MONGO_URI")

class BaseConfig(Config):
    '''Base config'''
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/database.db'
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DEBUG =True


class secret(Config):
     SECRET_KEY = os.environ.get("SECRET_KEY")
    
class TestConfig(Config):
    '''
    Test Configuration
    '''
    SQLALCHEMY_DATABASE_URI = 'sqlite:///testdatabase.db'
    SECRET_KEY = 'mysecretkey'
    TESTING = True
    WTF_CSRF_ENABLED = True
    DEBUG = True

config = {
    'Base': BaseConfig,
    'Test': TestConfig,
    'session':SessionConfig,
    'mail':MailConig,
    'upload': FileUpload,
    'mongo': dbMongo,
    'secret':secret
}