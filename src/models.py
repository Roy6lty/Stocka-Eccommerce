from src import app
from src import db

class user(db.Model):
      # database_model for user data
    id =db.Column(db.Integer(),primary_key=True)
    username=db.Column(db.String(length=30),unique=True,nullable=False)
    email=db.Column(db.String(length=50),unique=True,nullable=False)
    password_hash=db.Column(db.String(length=60),nullable=False)
    budget=db.Column(db.Integer(),nullable=False,default=1000)
    items=db.relationship('Item',backref='own_user',lazy=True)
   
    def __init__(self,username, email,password_hash)-> None:
        self.email = email
        self.username = username
        self.password_hash = password_hash
        #self.budget = budget

    def create_acc(self):
        with app.app_context():
            db.session.add(self)
            db.session.commit()
            


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
        new_item = Item(self.name, self.price, self.barcode, self.description,)
        with app.app_context():
            db.session.add(new_item)
            db.session.commit()


    def remove_item(self):
        existing_item = Item(self.name, self.barcode, self.description, self.price)
        with app.app_context():
            db.session.delete(existing_item)
            db.session.commit()
  



