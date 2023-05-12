from flask import Blueprint, Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

app = Flask(__name__,instance_relative_config=True)
app.config.from_object('config.Config') #base configuration 
app.config.from_object('config.SessionConfig')

db=SQLAlchemy(app) # initilizing the model object

bcrypt=Bcrypt(app)
Session(app)
login_manger= LoginManager(app)
login_manger.login_view = 'login_page'
login_manger.login_message_category = 'info'

from src import models

# initilzing Database
with app.app_context():
            db.create_all()
            

from src import routes
