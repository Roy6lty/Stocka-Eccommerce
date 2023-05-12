from dotenv import load_dotenv
import os
import redis
from datetime import timedelta

load_dotenv()
class Config(object):
    '''Base config'''
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SECRET_KEY = '89a9e0123ee2b43fa3a25d7f'
    DEBUG =True
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
    PERMANENT_SESSION_LIFETIME = timedelta(days=5)


    