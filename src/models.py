from flask import redirect, current_app as app
from .extentions import db, bcrypt, login_manger
from flask import jsonify
from flask_security import RoleMixin
from flask_login import UserMixin, current_user
from functools import wraps
import jwt
import uuid
from datetime import datetime, timezone, timedelta


roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
    )


@login_manger.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) # user method

class User(db.Model, UserMixin):
    """_summary_

    Args:
        db (_type_): _description_
        UserMixin (_type_): _description_
    """
      # database_model for user data
    id= db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20), unique =True)
    email = db.Column(db.String(50), nullable=False, unique= True)
    password_hash = db.Column(db.String(20), nullable=False)  
    cart_id = db.Column(db.String(20)) 
    address = db.Column(db.String(50)) 
    moblieno = db.Column(db.String(20))
    image_file=db.Column(db.String(60),nullable = False, default="default.png") 
    active = db.Column(db.Boolean())
    shop_id = db.Column(db.String(20))
    shopname = db.Column(db.String(20))
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
   
    def __init__(self,username:str, email:str, password_hash:str)-> None: #initilzing db Obj
        self.email = email
        self.username = username
        self.password = password_hash
        self.cart_id = str(uuid.uuid4())
    
    
    @property
    def password(self): #password getter from form
        return self.password_hash
    
    @password.setter
    def password(self, password_hash): 
        '''
        This function hashes the User passowrd
        '''
       
        self.password_hash = bcrypt.generate_password_hash(password_hash).decode('utf-8')
    
    @property
    def prettier_budget(self):
        '''
        returning commas between zeros for budget
        '''
        if len(str(self.budget)) >= 4:
            return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}'
        else:
            return f'{self.budget}'

    
    @staticmethod
    def token_encoder(*args, **kwargs):
        token = jwt.encode({
                    'expiration': str(datetime.now(tz=timezone.utc) + timedelta(seconds = 300)),
                    **kwargs
                },
                app.config['SECRET_KEY']
                )
        return token
    
    @staticmethod
    def token_decoder(token):
        payload = jwt.decode(
            token,
            key = app.config['SECRET_KEY']
        )

        return jsonify(payload, status = 200 )

    def has_role(self, role_name):
        my_role= Role.query.filter_by(name=role_name).first()
        if my_role in self.roles:
            return True
        else:
            return False    
    
    def create_account(self)-> None:
            with app.app_context():
                db.session.add(self)
                db.session.commit()

    def check_password_correction(self,  attempted_password)->None:
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

            


class Role(db.Model, RoleMixin):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

    def __init__(self, name:str):
        self.name = name

    def create_role(self):
            db.session.add(self)
            db.session.commit()

    def __repr__(self):
        return f'{self.name},{self.id}'
    
    def create_item(self):
        with app.app_context():
            db.session.add(self)
            db.session.commit()


class RoleUser:     
    def __init__():
        pass

    @staticmethod    
    def db_load(app,db):
        '''
        pre-populate the role table
        '''
        query =Role.query.count()
        if query == 0:
            merchant = Role(name="merchant")
            customer = Role(name="customer")
            admin = User(username="Admin", password_hash='123456',  email="olowoleru@gmail.com")
            db.session.add(merchant)
            db.session.add(customer)
            db.session.add(admin)
            db.session.commit()

            user = User.query.filter_by(email = 'olowoleru@gmail.com').first()
            role = Role.query.filter_by(name = 'merchant').first()
            user.roles.append(role) #assing role
            db.session.commit()


        

    
    def AssignRole(email:str, role:str):
       '''
       Assign roles for users
       '''
       user = User.query.filter_by(email = email).first()
       role = Role.query.filter_by(name = role).first()
       user.roles.append(role) #assing role
       db.session.commit() #terminate session

def require_role(role:str):
    """Checks assigned role for certain views 
    // Decorates view functions
    Args:
        role (Str): Role assigned to the user at registration
    """

    def decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            if not current_user.has_role(role):
                return app.login_manager.unauthorized()
            else:
                return func(*args, **kwargs)
        return wrapped_function
    return decorator
            
            

    


    

   



