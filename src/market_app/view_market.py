from ..extentions import db
from flask import render_template, redirect, url_for, flash, request,session, Blueprint
#from ..forms import RegisteredForm, LoginForm, Purchaseitemform
from flask_login import  login_required, current_user

app_market = Blueprint('app_market', __name__, static_folder="static", template_folder="market_templates",static_url_path='src/market_app/static')



@app_market.route('/market', methods = ['POST','GET'])
@login_required
def market_page():
    # form = Purchaseitemform()
    # items = Item.query.all()
    # if form.validate_on_submit():
    #     purchased_item =request.form.get('purchased_item')
    #     p_item_object = Item.query.filter_by(name= purchased_item).first()
    #     if p_item_object:
    #         p_item_object.owner = current_user.id
    #         current_user.budget-= p_item_object.price
    #         db.session.commit()
    #         flash(f'congratulations Your {purchased_item} was successful', category='success')
    
    #return render_template('market.html',items=items, form=form)
    return 'Market_page'


