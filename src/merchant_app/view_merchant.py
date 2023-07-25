from ..extentions import  mongo, client
from ..models import require_role,User
from ..utils import save_picture
from flask import render_template, redirect, url_for, flash, request,session, Blueprint, g, current_app
from ..forms import LoginForm,Add_product
from flask_login import  login_required, login_user, current_user
from ..MongoCRUD import Struct, StockaProducts, StockaShops
from bson.objectid import ObjectId
from datetime import datetime, date
import  json

app_merchant = Blueprint('app_merchant', __name__, static_folder="static", 
                         template_folder="merchant_templates",static_url_path='src/merchant_app/static')




@app_merchant.route('/', methods = ["GET","POST"])
def merchant_home():
    form=LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.Username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.Password.data):
            login_user(attempted_user)
            session['name'] = attempted_user #setting session-name to username
            flash(f'Success! You are logged in as {attempted_user.username}', category='success')
            #logging.info(f'username{attempted_user}')
            return redirect(url_for('app_merchant.merchant_dashboard'))
        else:
            flash('Username and password do not match! Try again', category='danger')

    return render_template('login.html', form=form)

  

@app_merchant.route('/Registration', methods = ["GET","POST"])
def merchant_register():
    
    return "Login page"


@app_merchant.route('/login', methods = ["GET","POST"])
def merchant_login():
    return "Login page"


@app_merchant.route('/dashboard')
@login_required
@require_role(role="merchant")
def merchant_dashboard():

    return "welcome to your dashboard"


@app_merchant.route('/products')
@login_required
@require_role(role="merchant")
def merchant_products():
    items = StockaProducts.find().sort("_id", 1).limit(6) #returns a pymongo cursor object

    return render_template('products.html', title = "merchantproducts", items = items)




@app_merchant.route('/addproduct',  methods = ["GET","POST"])
@login_required
@require_role(role="merchant")
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
    
    

@app_merchant.route('/updateproduct/<product>',  methods = ["GET","POST"])
@login_required
@require_role(role="merchant")
def update_product(product):
    form= Add_product()
    item = Struct(StockaProducts.find_one({'_id': ObjectId(product)}))
    

    if form.validate_on_submit():
        output_size, save_path= (500, 500), 'product_app/static/product_pic'
        image = save_picture(form.Picture.data, save_path, output_size)
        StockaProducts.update_one({'_id': ObjectId(product)},{'$set':{"name":form.Name.data, 
                                                                      "barcode":form.Barcode.data,
                                                                      "price":form.Price.data,
                                                                      "stock":form.Stock.data,
                                                                      "image_file":image }})
        
        flash(f'Product Updated', category='success')
        redirect(url_for("app_merchant.update_product", product=product))
    
    elif request.method == 'GET' :
        form.Name.data=  item.name #updating username
        form.Barcode.data = item.barcode
        form.Price.data = item.price 
        form.Stock.data = item.stock
        form.Description.data = item.description
        #form.Picture = product.image_file

    return render_template('update_product.html', title = "updateproducts", items = item, form=form)
        



@app_merchant.route('/deleteproduct/<product>')
@login_required
@require_role(role="merchant")
def merchant_deleteproduct(product):
    StockaProducts.delete_one({'_id': ObjectId(product)})

    flash(f'Product Deleted', category='success')
    return redirect(url_for('app_merchant.merchant_products'))
        
    