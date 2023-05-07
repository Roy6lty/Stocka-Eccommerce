from dotenv import load_dotenv
import os

load_dotenv()
class Config(object):
    SQLACHEMY_DATABASE_URI = 'sqlite///database.db'
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG =True
    