from flask import Blueprint, Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__,instance_relative_config=True)
app.config.from_object('config.Config')
#app.run(debug=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
from src import models

# initilzing Database
with app.app_context():
            db.create_all()


from src import routes
