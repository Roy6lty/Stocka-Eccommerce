from ..extentions import db
from flask import render_template, redirect, url_for, flash, request,session, Blueprint
from ..models import user, Item
from ..utils import save_picture
from ..forms import Add_product, Comments
from flask_login import  login_required, current_user

app_product = Blueprint('app_product', __name__, static_folder="static", template_folder="product_templates",static_url_path='src/product_app/static')

@app_product.route('/add_product', methods = ['POST','GET'])
def add_product():
    form= Add_product()

    if   request.method == 'POST' and form.validate(): #validation of data entry
            #logging.info(form.Email_address.data)
            output_size, save_path= (500, 500), 'product_app/static/product_pic'
            image = save_picture(form.Picture.data, save_path, output_size)
            product_to_create = Item(name=form.Name.data, #db session object created
                                price=form.Price.data,
                                barcode=form.Barcode.data,
                                stock=form.Stock.data,
                                description=form.Description.data,
                                image_file = image
                                )
            product_to_create.create_item()
            flash(f'Congratulations! You have successfully Added your product', category='success')
            return redirect(url_for('app_product.add_product'))
      
    if form.errors != {}:
        for err_msg in form.errors.items():
            print(form.errors.values())
            flash(f':{err_msg}',category='danger')

    return render_template('add_product.html', title = "Add_Product", form = form)


@app_product.route('/shopping', methods=['POST','GET'])
def shopping_page():
    items = Item.query.all()
    return render_template('shopping.html', title = "shopping", items = items)


@app_product.route('/<item>', methods=['POST','GET'])
def product_page(item):
    form= Comments()
    product_id=item[-1]

    product = Item.query.filter_by(id=product_id).first()
    
    
    return render_template('product_page.html', item=product, form=form)
