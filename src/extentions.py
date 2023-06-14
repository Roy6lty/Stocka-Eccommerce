from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename

db = SQLAlchemy()
mail = Mail()
login_manger = LoginManager()
bcrypt=Bcrypt()
session  = Session()
