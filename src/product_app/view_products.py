from ..extentions import  redis_connector, mongo, client
from flask import render_template, redirect, url_for, flash, request,session, Blueprint, g, current_app
from ..utils import save_picture
from ..forms import Add_product, Comments, AddToCart
from flask_login import  login_required, current_user
from ..cart import Shoppingcart, CartId, AddItem, DeleteItem
from .. MongoCRUD import Struct, StockaProducts
from bson.objectid import ObjectId
from datetime import datetime, date

app_product = Blueprint('app_product', __name__, static_folder="static", template_folder="product_templates",static_url_path='src/product_app/static')

@app_product.route('/add_product', methods = ['POST','GET'])
def add_product():
    form= Add_product()
    
    if   request.method == 'POST' and form.validate(): #validation of data entry
                #logging.info(form.Email_address.data)
                output_size, save_path= (500, 500), 'product_app/static/product_pic'
                image = save_picture(form.Picture.data, save_path, output_size)
                StockaProducts.insert_one({'name':form.Name.data, #db session object created
                                    'price':form.Price.data,
                                    'barcode':form.Barcode.data,
                                    'stock':form.Stock.data,
                                    'description':form.Description.data,
                                    'image_file' : image,
                                    'reviews':[],
                                    'date':datetime.now()})
                flash(f'Congratulations! You have successfully Added your product', category='success')
            
                return redirect(url_for('app_product.add_product'))
        
    if form.errors != {}:
        for err_msg in form.errors.items():
            print(form.errors.values())
            flash(f':{err_msg}',category='danger')


    return render_template('add_product.html', title = "Add_Product", form = form)



@app_product.route('/', methods=['GET'])
@CartId
def shopping_page():
    items = list(StockaProducts.find())
    items = Struct.submit(items)
    print(current_app.root_path)
    return render_template('shopping.html', title = "shopping", items = items)




@app_product.route('/<item>', methods=['POST','GET'])
@CartId
def product_page(item):
    form = Comments()
   
    product  = Struct(
         StockaProducts.find_one({'_id':ObjectId(item)})
         )
    ProductComment = product.reviews
    cart_id = request.cookies.get('cart_id')
    if   request.method == 'POST':
        if form.Submit.data and form.Description.data:
            if current_user.is_authenticated:
                StockaProducts.update_one({"_id":ObjectId(item)},
                                                {'$push': {'reviews':{'name': current_user.username, 
                                                                      'body':form.Description.data,
                                                                      "date":datetime.now()}}})
                flash(f'Comment posted', category='success')
                redirect(url_for('app_product.product_page', item=product, form=form, productcomment=ProductComment)) #reload page
            else: flash(f'Signin to comment', category='warning')

        elif form.Addtocart.data:
           AddItem(redis_connector, cart_id, item)#add to redis dataase 
           flash(f'Your item has been successfully Added your cart', category='success')
        
    return render_template('product_page.html', item=product, form=form, productcomment=ProductComment )



@app_product.route('delete/<cartitem>/<page_function>', methods=['POST','GET'])
def unload_cart(cartitem, page_function):
    
    cart_id = request.cookies.get('cart_id')
    DeleteItem(redis_connector, cart_id, cartitem)#add to redis dataase 
    flash(f'item removed from cart', category='success')
    return redirect(url_for( page_function, item=cartitem))


#nosql Database Add
@app_product.route('/original', methods=['POST','GET'])
def add_mongo():
    form= Comments()
    
    if   request.method == 'POST' and form.validate(): #validation of data entry
                #logging.info(form.Email_address.data)
                output_size, save_path= (500, 500), 'product_app/static/product_pic'
                image = save_picture(form.Picture.data, save_path, output_size)
                StockaProducts.insert_one({'name':form.Name.data, #db session object created
                                    'price':form.Price.data,
                                    'barcode':form.Barcode.data,
                                    'stock':form.Stock.data,
                                    'description':form.Description.data,
                                    'image_file' : image})
                flash(f'Congratulations! You have successfully Added your product', category='success')
            
                return redirect(url_for('app_product.add_product'))
        
    if form.errors != {}:
        for err_msg in form.errors.items():
            print(form.errors.values())
            flash(f':{err_msg}',category='danger')

    return render_template('add_product.html', title = "Add_Product", form = form)


app_product.route('/tired', methods=['GET', "POST"])
def brandnew():
    form= Add_product()
    StockaProduct = client.stocka.products
    items = StockaProduct.find_one({'_id': "64afc9d562fd7c96e935b984"})
    return render_template('shopping.html', title = "shopping", items = items, form = form)
 