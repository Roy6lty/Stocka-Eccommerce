from flask import current_app as app
from .extentions import db, bcrypt, login_manger
from flask import jsonify
from flask_login import UserMixin
import jwt
from datetime import datetime, timezone, timedelta





@login_manger.user_loader
def load_user(user_id):
    return user.query.get(int(user_id)) # user method

class user(db.Model, UserMixin):
    """_summary_

    Args:
        db (_type_): _description_
        UserMixin (_type_): _description_
    """
      # database_model for user data
    id =db.Column(db.Integer(),primary_key=True)
    username=db.Column(db.String(length=30),unique=True,nullable=False)
    email=db.Column(db.String(length=50),unique=True,nullable=False)
    password_hash=db.Column(db.String(length=60),nullable=False)
    budget=db.Column(db.Integer(),nullable=False,default=1000)
    image_file=db.Column(db.String(60), nullable=False, default = "default.png")
    items=db.relationship('Item',backref='own_user',lazy=True)
   
    def __init__(self,username:str, email:str, password_hash:str)-> None: #initilzing db Obj
        self.email = email
        self.username = username
        self.password = password_hash
    
    
    @property
    def password(self): #password getter from form
        return self.password_hash
    
    @password.setter
    def password(self, password_hash): 
        '''
        This function hashes the User passowrd
        '''
        print(password_hash)
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
    
    
    def create_account(self)-> None:
            with app.app_context():
                db.session.add(self)
                db.session.commit()

    def check_password_correction(self,  attempted_password)->None:
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

            


class Item(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    name= db.Column(db.String(length=30),nullable= False, unique=True)
    price=db.Column(db.Integer(),nullable=False)
    barcode=db.Column(db.String(60))
    description=db.Column(db.String(1024), nullable=False)
    stock= db.Column(db.Integer(), nullable=False)
    image_file=db.Column(db.String(60), nullable=False, default = "default.png")
    owner=db.Column(db.Integer(),db.ForeignKey('user.id'))

    def __init__(self,name:str, price:int, barcode:str, stock:int, description:str, image_file:str) -> None:
        self.name= name
        self.barcode = barcode
        self.price = price
        self.stock = stock
        self.description = description
        self.image_file = image_file

    # @property
    # def barcode(self): #barcode getter from form
    #     return self.barcode
    
    # @barcode.setter
    # def barcode(self, barcode): 
    #     '''
    #     This function hashes the User passowrd
    #     '''
    #     if barcode:
    #             self.barcode = barcode
    #             return self.barcode 
    #     else:
    #         self.barcode = None
    #         return self.barcode
        

    def __repr__(self):
        return f'{self.name},{self.id}'
    
    def create_item(self):
        with app.app_context():
            db.session.add(self)
            db.session.commit()


    def remove_item(self):
        existing_item = Item(self.name, self.barcode, self.description, self.price)
        with app.app_context():
            db.session.delete(existing_item)
            db.session.commit()
    

   



