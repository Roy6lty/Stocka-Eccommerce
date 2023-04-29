from src import app
from src.models import Item

if __name__ == '__main__':
    app.run(debug=True)

    _id = Item(name='samsung',description='brand_new',price=400,barcode='21433452235363')
    _id.create_item()
    print('into')




    