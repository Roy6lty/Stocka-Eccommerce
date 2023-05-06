from src import app, db, bcrypt, login_manger
from flask_login import UserMixin


@login_manger.user_loader
def load_user(user_id):
    return user.query.get(int(user_id))

class user(db.Model, UserMixin):
      # database_model for user data
    id =db.Column(db.Integer(),primary_key=True)
    username=db.Column(db.String(length=30),unique=True,nullable=False)
    email=db.Column(db.String(length=50),unique=True,nullable=False)
    password_hash=db.Column(db.String(length=60),nullable=False)
    budget=db.Column(db.Integer(),nullable=False,default=1000)
    items=db.relationship('Item',backref='own_user',lazy=True)
   
    def __init__(self,username, email, password_hash)-> None: #initilzing db Obj
        self.email = email
        self.username = username
        self.password = password_hash
    
    
    @property
    def password(self): #password getter from form
        return self.password_hash
    
    @password.setter
    def password(self, plain_text_password): 
        '''
        This function hashes the User passowrd
        '''
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    
    @property
    def prettier_budget(self):
        '''
        returning commas between zeros for budget
        '''
        if len(str(self.budget)) >= 4:
            return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}'
        else:
            return f'{self.budget}'
    
    
       
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
    barcode=db.Column(db.String(length=12), nullable=False)
    description=db.Column(db.String(1024), nullable=False)
    owner=db.Column(db.Integer(),db.ForeignKey('user.id'))

    def __init__(self,name, price, barcode, description)-> None:
        self.name= name
        self.barcode = barcode
        self.price = price
        self.description = description

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
    

   



