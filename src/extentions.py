from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
from flask_pymongo import PyMongo
#from werkzeug.middleware.profiler import ProfileMiddleware
import redis
redis_connector = redis.Redis(host='localhost', port=6379, decode_responses=True)
from pymongo import MongoClient 
#from .config import dbMongo

#pymongo

#connection_string = dbMongo.MONGO_URI
connection_string =f"mongodb://localhost:27017"
client = MongoClient(connection_string)



# initilaztion
db = SQLAlchemy()
mail = Mail()
login_manger = LoginManager()
bcrypt=Bcrypt()
session  = Session()
mongo = PyMongo()
