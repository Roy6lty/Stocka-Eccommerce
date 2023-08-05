from ..utils import tokens
from flask import request, render_template, redirect, url_for, Blueprint, current_app as app
from ..MongoCRUD import StockaProducts, Struct
from ..forms import AccountUpdate
from docxtpl import DocxTemplate, InlineImage
from flask_login import login_required, current_user
from ..cart import RetrieveCart
from datetime import date
from ..MongoCRUD import Struct
from tasks import GetReceipt

app_checkout = Blueprint('app_checkout', __name__, static_folder="static", template_folder="checkout_templates",static_url_path='src/checkout_app/static')


@app_checkout.route('/', methods = ['GET','POST'])
@login_required
def complete_checkout():
    form = AccountUpdate()
    cart = RetrieveCart() #returns a zip iterable
    salesRows = []
    item_total = 0 
    checkout_total = 0
    for item, quantity in cart: 
        checkout_total += int(item['price']) * int(quantity)
        item_total += 1
        sale = {"name":item['name'], "quantity":quantity, "price":item['price'], "total" : int(item['price']) *int( quantity)}
        salesRows.append(sale) 

    #celery json obj
    celery_json = {"SalesRow":salesRows, "checkout_total":checkout_total, 
                    "username":current_user.username, "address":current_user.address, 
                    "phoneno" :current_user.moblieno}

    #
    
        
        


    if request.method == 'POST':
         #current_user.moblieno = form.Mobile_number.data #updating username
         current_user.address = form.Address.data 
         current_user.state  = form.State.data 
         current_user.country = form.Country.data 

         redirect(url_for('app_checkout.checkout'))

    elif request.method == 'GET':

        form.Mobile_number.data=  current_user.moblieno #updating username
        form.Address.data = current_user.address
        # form.State.data = current_user.State 
        # form.Country.data = current_user.Country
        #form.Picture = product.image_file
        #GetReceipt.delay(celery_json)
        
        

    return render_template("complete_checkout.html", form=form, cart_checkout= RetrieveCart(), 
                                    item_total=item_total, checkout_total=checkout_total)





@login_required
@app_checkout.route('/checkout/<cart>')
def checkout(cart):
    doc = DocxTemplate("stockinvoice.docx") #receipt document
       
    salesRows=[]  #intilazing values
    checkout_total = 0  
    invoice = tokens()

    for item, quantity in cart: 
        checkout_total += int(item['price']) * int(quantity)
        sale = {"name":item['name'], "quantity":quantity, "price":item['price'], "total" : int(item['price']) * quantity}
        salesRows.append(sale) 
        #[sale for item, quanity in cart ]
    
    context ={
    "invoice_id" : invoice,
    "date" : date.today(),
    "recipent": current_user.username,
    "address": current_user.address,
    "phone": current_user.phoneno,
    "salesTbRows": salesRows,
    "subtotal": checkout_total,
    "total": checkout_total
    }
 
    doc.render(context)
    filename = f'{invoice}.docx' #generating username
    doc.save(filename)

    return "<h1> Your has been Completed </h1>"