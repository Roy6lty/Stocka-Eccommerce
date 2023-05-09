from src import app
from src import db
from src.models import Item, user


#_id = user(username='Olowoleru',email='olowoleru06@gmail', password_hash= 'omotola')
# _id = Item(price= 1500,name= 'samsung',barcode='353samsung222', description='am tired sam')
# _id.create_item()
# print('into')
# with app.app_context():
#     item1 = Item.query.filter_by(name= 'blackberry').first()
#     item1.owner = user.query.filter_by(username='Olowoleru').first().id
#     db.session.add(item1)
#     db.session.commit()
    
# with app.app_context():
#     item1 = Item.query.filter_by(name= 'blackberry').first()
    
# print(item1.owner)

item1 = Item(name= 'pixel_6',price=250, barcode='pixel61234',description='Brand new pixel6')
item1.create_item()
